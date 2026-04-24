import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';
import matter from 'gray-matter';
import { marked } from 'marked';

const CHANNEL = '@gaperton_tech';
const BASE = join(process.cwd(), '..', 'tg-export', CHANNEL);
const REPO_BASE = `https://raw.githubusercontent.com/gaperton/gaperton.github.io/main/tg-export/${CHANNEL}`;

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
}

export interface Comment {
  id: number;
  date: string;
  author: string;
  authorHandle?: string;
  bodyHtml: string;
  images: string[];
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
// Quote any frontmatter value that starts with @ before parsing.
function fixFrontmatter(raw: string): string {
  return raw.replace(/^([ \t]*[\w_]+:\s*)(@\S+)/gm, '$1"$2"');
}

function renderMarkdown(src: string): string {
  return marked.parse(src) as string;
}

function textPreview(src: string, len = 300): string {
  // strip markdown syntax for a plain text preview
  return src
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/#{1,6}\s/g, '')
    .replace(/[*_`~]/g, '')
    .trim()
    .slice(0, len);
}

export function getMonths(): string[] {
  if (!existsSync(BASE)) return [];
  return readdirSync(BASE)
    .filter(isMonthDir)
    .sort();
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
      days.add(slugToDate(slug));
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
  // date is "YYYY-MM-DD", month dir is "YYYY-MM"
  const month = date.slice(0, 7);
  const slugs = getPostSlugsForMonth(month).filter(s => s.startsWith(date));
  return slugs.map(slug => {
    const raw = readFileSync(join(BASE, month, `${slug}.md`), 'utf-8');
    const { data, content } = matter(fixFrontmatter(raw));
    return {
      slug,
      month,
      date,
      datetime: String(data.date),
      id: Number(data.id),
      preview: textPreview(content),
      commentCount: countComments(month, slug),
      hasImages: hasImages(month, slug),
    };
  }).sort((a, b) => a.id - b.id);
}

export function getPostsForMonth(month: string): Post[] {
  return getPostSlugsForMonth(month).map(slug => {
    const raw = readFileSync(join(BASE, month, `${slug}.md`), 'utf-8');
    const { data, content } = matter(fixFrontmatter(raw));
    return {
      slug,
      month,
      date: slugToDate(slug),
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
      });
    }
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
  };
}
