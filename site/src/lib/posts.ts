import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';
import matter from 'gray-matter';
import { marked } from 'marked';

const CHANNEL = '@gaperton_tech';
const BASE = join(process.cwd(), '..', 'tg-export', CHANNEL);
const REPO_BASE = `https://raw.githubusercontent.com/gaperton/gaperton.github.io/main/tg-export/${CHANNEL}`;

const DAY_START_HOUR = 4;

// Returns "YYYY-MM-DD" in local timezone, with day starting at DAY_START_HOUR.
function computeLogicalDay(isoDatetime: string): string {
  const dt = new Date(isoDatetime);
  // Shift back by DAY_START_HOUR hours so that e.g. 3:59 local → previous day
  const shifted = new Date(dt.getTime() - DAY_START_HOUR * 60 * 60 * 1000);
  const y = shifted.getFullYear();
  const m = String(shifted.getMonth() + 1).padStart(2, '0');
  const d = String(shifted.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export interface Post {
  slug: string;      // e.g. "2022-09-21_5"
  month: string;     // e.g. "2022-09"
  date: string;      // e.g. "2022-09-21"
  datetime: string;  // full ISO string from frontmatter, e.g. "2022-09-21T03:08:09+00:00"
  id: number;
  preview: string;
  commentCount: number;
  hasImages: boolean;
}

export interface PostDetail {
  slug: string;
  month: string;
  date: string;
  datetime: string;
  id: number;
  bodyHtml: string;
  images: string[];
  comments: Comment[];
  replyQuote?: string;  // exact quoted text from reply_quote field
}

export interface Comment {
  id: number;
  date: string;
  author: string;
  authorHandle?: string;
  bodyHtml: string;
  images: string[];
  replyTo?: { author: string; preview: string };
}

function isMonthDir(name: string): boolean {
  return /^\d{4}-\d{2}$/.test(name);
}

function isPostFile(name: string): boolean {
  return /^\d{4}-\d{2}-\d{2}_\d+\.md$/.test(name);
}

function slugToDate(slug: string): string {
  return slug.slice(0, 10); // "YYYY-MM-DD"
}

// gray-matter uses js-yaml which rejects bare @ values (YAML reserved).
// Also single-quote reply_quote values which may contain colons, double-quotes, etc.
function fixFrontmatter(raw: string): string {
  return raw
    .replace(/^([ \t]*[\w_]+:\s*)(@\S+)/gm, '$1"$2"')
    .replace(/^(reply_quote:\s*)(.+)$/gm, (_match, key, val) => {
      if (val.startsWith("'")) return _match; // already single-quoted
      const escaped = val.replace(/'/g, "''");
      return `${key}'${escaped}'`;
    });
}

marked.setOptions({ breaks: true });

// Lazy map: Telegram post ID → local URL path
let _postIdMap: Map<number, string> | null = null;
function getPostIdMap(): Map<number, string> {
  if (_postIdMap) return _postIdMap;
  _postIdMap = new Map();
  for (const month of getMonths()) {
    for (const slug of getPostSlugsForMonth(month)) {
      const id = Number(slug.split('_').pop());
      if (!isNaN(id)) _postIdMap.set(id, `/${month}/${slug}/`);
    }
  }
  return _postIdMap;
}

marked.use({
  walkTokens(token: any) {
    if (token.type === 'link' && token.href) {
      const m = token.href.match(/t\.me\/gaperton_tech\/(\d+)/i);
      if (m) {
        const local = getPostIdMap().get(Number(m[1]));
        if (local) token.href = local;
      }
    }
  },
});

function renderMarkdown(src: string): string {
  return marked.parse(src) as string;
}

function textPreview(src: string, len = 300): string {
  const text = src
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/#{1,6}\s/g, '')
    .replace(/[*_`~]/g, '')
    .trim();
  return text.length > len ? text.slice(0, len) + ' [...]' : text;
}

export function getMonths(): string[] {
  if (!existsSync(BASE)) return [];
  return readdirSync(BASE)
    .filter(isMonthDir)
    .sort();
}

function findPostPreviewById(id: number): string | undefined {
  for (const month of getMonths()) {
    const dir = join(BASE, month);
    const match = readdirSync(dir).find(f => f === `${f.slice(0, 10)}_${id}.md` || f.endsWith(`_${id}.md`));
    if (match) {
      const raw = readFileSync(join(dir, match), 'utf-8');
      const { content } = matter(fixFrontmatter(raw));
      const preview = textPreview(content, 200);
      return preview || undefined;
    }
  }
  return undefined;
}

export function getPostSlugsForMonth(month: string): string[] {
  const dir = join(BASE, month);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter(isPostFile)
    .map(f => basename(f, '.md'))
    .sort();
}

export function getAllDays(): string[] {
  const days = new Set<string>();
  for (const month of getMonths()) {
    for (const slug of getPostSlugsForMonth(month)) {
      const raw = readFileSync(join(BASE, month, `${slug}.md`), 'utf-8');
      const { data } = matter(fixFrontmatter(raw));
      if (data.date) days.add(computeLogicalDay(String(data.date)));
    }
  }
  return [...days].sort().reverse();
}

function countComments(month: string, slug: string): number {
  const dir = join(BASE, month, `${slug}.comments`);
  if (!existsSync(dir)) return 0;
  return readdirSync(dir).filter(f => f.endsWith('.md')).length;
}

function hasImages(month: string, slug: string): boolean {
  const dir = join(BASE, month, `${slug}.files`);
  if (!existsSync(dir)) return false;
  return readdirSync(dir).some(f => /\.(jpg|jpeg|png|gif|webp)$/i.test(f));
}

export function getPostsForDay(date: string): Post[] {
  // Scan the month matching the date and adjacent months (timezone shift can cross month boundary)
  const [year, mon] = date.split('-').map(Number);
  const monthsToScan = new Set<string>();
  monthsToScan.add(`${year}-${String(mon).padStart(2, '0')}`);
  const prevMon = mon === 1 ? `${year - 1}-12` : `${year}-${String(mon - 1).padStart(2, '0')}`;
  const nextMon = mon === 12 ? `${year + 1}-01` : `${year}-${String(mon + 1).padStart(2, '0')}`;
  monthsToScan.add(prevMon);
  monthsToScan.add(nextMon);

  const result: Post[] = [];
  for (const month of monthsToScan) {
    for (const slug of getPostSlugsForMonth(month)) {
      const raw = readFileSync(join(BASE, month, `${slug}.md`), 'utf-8');
      const { data, content } = matter(fixFrontmatter(raw));
      if (!data.date) continue;
      if (computeLogicalDay(String(data.date)) !== date) continue;
      result.push({
        slug,
        month,
        date,
        datetime: String(data.date),
        id: Number(data.id),
        preview: textPreview(content),
        commentCount: countComments(month, slug),
        hasImages: hasImages(month, slug),
      });
    }
  }
  return result.sort((a, b) => a.id - b.id);
}

export function getPostsForMonth(month: string): Post[] {
  return getPostSlugsForMonth(month).map(slug => {
    const raw = readFileSync(join(BASE, month, `${slug}.md`), 'utf-8');
    const { data, content } = matter(fixFrontmatter(raw));
    return {
      slug,
      month,
      date: data.date ? computeLogicalDay(String(data.date)) : slugToDate(slug),
      datetime: String(data.date),
      id: Number(data.id),
      preview: textPreview(content),
      commentCount: countComments(month, slug),
      hasImages: hasImages(month, slug),
    };
  });
}

function getImageFiles(month: string, slug: string): string[] {
  const dir = join(BASE, month, `${slug}.files`);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter(f => /\.(jpg|jpeg|png|gif|webp)$/i.test(f))
    .map(f => `${REPO_BASE}/${month}/${slug}.files/${f}`);
}

function getCommentImages(month: string, slug: string, commentFileBase: string): string[] {
  const dir = join(BASE, month, `${slug}.comments`);
  if (!existsSync(dir)) return [];
  // image files are named "{commentId}-{filename}.ext", not "{commentId}-{author}-..."
  const commentId = commentFileBase.split('-')[0];
  const prefix = commentId + '-';
  return readdirSync(dir)
    .filter(f => f.startsWith(prefix) && /\.(jpg|jpeg|png|gif|webp)$/i.test(f))
    .map(f => `${REPO_BASE}/${month}/${slug}.comments/${f}`);
}

export function getPost(month: string, slug: string): PostDetail {
  const raw = readFileSync(join(BASE, month, `${slug}.md`), 'utf-8');
  const { data, content } = matter(fixFrontmatter(raw));

  const commentsDir = join(BASE, month, `${slug}.comments`);
  const comments: Comment[] = [];

  if (existsSync(commentsDir)) {
    const commentFiles = readdirSync(commentsDir)
      .filter(f => f.endsWith('.md'))
      .sort((a, b) => {
        const idA = parseInt(a.split('-')[0], 10);
        const idB = parseInt(b.split('-')[0], 10);
        return idA - idB;
      });

    for (const cf of commentFiles) {
      const craw = readFileSync(join(commentsDir, cf), 'utf-8');
      const { data: cd, content: cc } = matter(fixFrontmatter(craw));
      const fileBase = basename(cf, '.md');
      comments.push({
        id: Number(cd.id),
        date: String(cd.date),
        author: String(cd.author ?? 'unknown'),
        authorHandle: cd.author_handle ? String(cd.author_handle) : undefined,
        bodyHtml: renderMarkdown(cc),
        images: getCommentImages(month, slug, fileBase),
        _replyToId: cd.reply_to ? Number(cd.reply_to) : undefined,
        _replyQuote: cd.reply_quote ? String(cd.reply_quote) : undefined,
      } as Comment & { _replyToId?: number; _replyQuote?: string });
    }
  }

  // Resolve reply_to references
  type Tmp = Comment & { _replyToId?: number; _replyQuote?: string };
  const byId = new Map(comments.map(c => [c.id, c]));
  for (const c of comments as Tmp[]) {
    if (c._replyToId) {
      const explicitQuote = c._replyQuote;
      const ref = byId.get(c._replyToId);
      // prefer the exact selected quote; fall back to first 160 chars of the referenced message
      const refText = ref?.bodyHtml.replace(/<[^>]+>/g, '').trim() ?? '';
      const preview = explicitQuote ?? (refText ? textPreview(refText, 160) : undefined);
      if (preview) {
        c.replyTo = { author: ref?.author ?? '…', preview };
      }
    }
    delete c._replyToId;
    delete c._replyQuote;
  }

  return {
    slug,
    month,
    date: slugToDate(slug),
    datetime: String(data.date),
    id: Number(data.id),
    bodyHtml: renderMarkdown(content),
    images: getImageFiles(month, slug),
    comments,
    replyQuote: data.reply_quote
      ? String(data.reply_quote)
      : data.reply_to
        ? findPostPreviewById(Number(data.reply_to))
        : undefined,
  };
}
