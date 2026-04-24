import { c as createComponent, m as maybeRenderHead, d as addAttribute, a as renderTemplate, b as createAstro, r as renderComponent, e as renderHead, f as renderSlot } from './astro/server_bxzVAHRU.mjs';
import 'kleur/colors';
import 'clsx';
/* empty css                          */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, basename } from 'node:path';
import matter from 'gray-matter';
import { marked } from 'marked';

const $$Astro$2 = createAstro();
const $$MiniCalendar = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$2, $$props, $$slots);
  Astro2.self = $$MiniCalendar;
  const { month, posts, prevMonth = null, nextMonth = null } = Astro2.props;
  const [year, mon] = month.split("-").map(Number);
  const daysInMonth = new Date(year, mon, 0).getDate();
  const firstDow = new Date(year, mon - 1, 1).getDay();
  const offset = (firstDow + 6) % 7;
  const activeDays = new Set(posts.map((p) => p.date));
  const label = new Date(year, mon - 1, 1).toLocaleString("en-GB", { month: "long", year: "numeric" });
  return renderTemplate`${maybeRenderHead()}<div class="cal" data-astro-cid-guxmg3ij> <div class="cal-header" data-astro-cid-guxmg3ij> ${prevMonth ? renderTemplate`<a${addAttribute(`/${prevMonth}/`, "href")} class="nav" title="Previous month" data-astro-cid-guxmg3ij>‹</a>` : renderTemplate`<span class="nav disabled" data-astro-cid-guxmg3ij>‹</span>`} <span class="cal-title" data-astro-cid-guxmg3ij>${label}</span> ${nextMonth ? renderTemplate`<a${addAttribute(`/${nextMonth}/`, "href")} class="nav" title="Next month" data-astro-cid-guxmg3ij>›</a>` : renderTemplate`<span class="nav disabled" data-astro-cid-guxmg3ij>›</span>`} </div> <div class="cal-grid" data-astro-cid-guxmg3ij> ${["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map((d) => renderTemplate`<span class="dow" data-astro-cid-guxmg3ij>${d}</span>`)} ${Array.from({ length: offset }, (_, i) => renderTemplate`<span${addAttribute(`empty-${i}`, "key")} data-astro-cid-guxmg3ij></span>`)} ${Array.from({ length: daysInMonth }, (_, i) => {
    const day = i + 1;
    const dateStr = `${month}-${String(day).padStart(2, "0")}`;
    return activeDays.has(dateStr) ? renderTemplate`<a${addAttribute(`/${dateStr}/`, "href")} class="day active" data-astro-cid-guxmg3ij>${day}</a>` : renderTemplate`<span class="day" data-astro-cid-guxmg3ij>${day}</span>`;
  })} </div> </div> `;
}, "C:/Users/Vlad/GitHub/gaperton.github.io/site/src/components/MiniCalendar.astro", void 0);

const $$Astro$1 = createAstro();
const $$Sidebar = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$Sidebar;
  const { months, currentMonth, postsIndex } = Astro2.props;
  const idx = months.indexOf(currentMonth);
  const prevMonth = idx > 0 ? months[idx - 1] : null;
  const nextMonth = idx < months.length - 1 ? months[idx + 1] : null;
  const byYear = {};
  for (const m of [...months].reverse()) {
    const y = m.slice(0, 4);
    if (!byYear[y]) byYear[y] = [];
    byYear[y].push(m);
  }
  const years = Object.keys(byYear).sort().reverse();
  function monthLabel(m) {
    const [y, mo] = m.split("-").map(Number);
    return new Date(y, mo - 1, 1).toLocaleString("en-GB", { month: "long" });
  }
  return renderTemplate`${maybeRenderHead()}<div class="sidebar" data-astro-cid-ssfzsv2f> ${renderComponent($$result, "MiniCalendar", $$MiniCalendar, { "month": currentMonth, "posts": postsIndex[currentMonth] ?? [], "prevMonth": prevMonth, "nextMonth": nextMonth, "data-astro-cid-ssfzsv2f": true })} <div class="divider" data-astro-cid-ssfzsv2f></div> <nav class="archive" data-astro-cid-ssfzsv2f> <div class="archive-title" data-astro-cid-ssfzsv2f>Archive</div> ${years.map((year) => renderTemplate`<details${addAttribute(currentMonth.startsWith(year), "open")} data-astro-cid-ssfzsv2f> <summary class="year" data-astro-cid-ssfzsv2f>${year}</summary> <ul data-astro-cid-ssfzsv2f> ${byYear[year].map((m) => renderTemplate`<li data-astro-cid-ssfzsv2f> <a${addAttribute(`/${m}/`, "href")}${addAttribute([{ active: m === currentMonth }], "class:list")} data-astro-cid-ssfzsv2f>${monthLabel(m)}</a> </li>`)} </ul> </details>`)} </nav> </div> `;
}, "C:/Users/Vlad/GitHub/gaperton.github.io/site/src/components/Sidebar.astro", void 0);

const $$Astro = createAstro();
const $$Layout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Layout;
  const { title, sidebarMonths = [], currentMonth = "", postsIndex = {} } = Astro2.props;
  return renderTemplate`<html lang="en" data-astro-cid-sckkx6r4> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>${title}</title>${renderHead()}</head> <body data-astro-cid-sckkx6r4> <header data-astro-cid-sckkx6r4> <a href="/" class="brand" data-astro-cid-sckkx6r4>@gaperton_tech</a> <span class="tagline" data-astro-cid-sckkx6r4>Telegram channel archive</span> </header> <div class="layout" data-astro-cid-sckkx6r4> <aside data-astro-cid-sckkx6r4> ${renderComponent($$result, "Sidebar", $$Sidebar, { "months": sidebarMonths, "currentMonth": currentMonth, "postsIndex": postsIndex, "data-astro-cid-sckkx6r4": true })} </aside> <main data-astro-cid-sckkx6r4> ${renderSlot($$result, $$slots["default"])} </main> </div> </body></html>`;
}, "C:/Users/Vlad/GitHub/gaperton.github.io/site/src/layouts/Layout.astro", void 0);

const CHANNEL = "@gaperton_tech";
const BASE = join(process.cwd(), "..", "tg-export", CHANNEL);
const REPO_BASE = `https://raw.githubusercontent.com/gaperton/gaperton.github.io/main/tg-export/${CHANNEL}`;
function isMonthDir(name) {
  return /^\d{4}-\d{2}$/.test(name);
}
function isPostFile(name) {
  return /^\d{4}-\d{2}-\d{2}_\d+\.md$/.test(name);
}
function slugToDate(slug) {
  return slug.slice(0, 10);
}
function fixFrontmatter(raw) {
  return raw.replace(/^([ \t]*[\w_]+:\s*)(@\S+)/gm, '$1"$2"');
}
function renderMarkdown(src) {
  return marked.parse(src);
}
function textPreview(src, len = 300) {
  return src.replace(/!\[.*?\]\(.*?\)/g, "").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/#{1,6}\s/g, "").replace(/[*_`~]/g, "").trim().slice(0, len);
}
function getMonths() {
  if (!existsSync(BASE)) return [];
  return readdirSync(BASE).filter(isMonthDir).sort();
}
function getPostSlugsForMonth(month) {
  const dir = join(BASE, month);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter(isPostFile).map((f) => basename(f, ".md")).sort();
}
function getAllDays() {
  const days = /* @__PURE__ */ new Set();
  for (const month of getMonths()) {
    for (const slug of getPostSlugsForMonth(month)) {
      days.add(slugToDate(slug));
    }
  }
  return [...days].sort().reverse();
}
function countComments(month, slug) {
  const dir = join(BASE, month, `${slug}.comments`);
  if (!existsSync(dir)) return 0;
  return readdirSync(dir).filter((f) => f.endsWith(".md")).length;
}
function hasImages(month, slug) {
  const dir = join(BASE, month, `${slug}.files`);
  if (!existsSync(dir)) return false;
  return readdirSync(dir).some((f) => /\.(jpg|jpeg|png|gif|webp)$/i.test(f));
}
function getPostsForDay(date) {
  const month = date.slice(0, 7);
  const slugs = getPostSlugsForMonth(month).filter((s) => s.startsWith(date));
  return slugs.map((slug) => {
    const raw = readFileSync(join(BASE, month, `${slug}.md`), "utf-8");
    const { data, content } = matter(fixFrontmatter(raw));
    return {
      slug,
      month,
      date,
      datetime: String(data.date),
      id: Number(data.id),
      preview: textPreview(content),
      commentCount: countComments(month, slug),
      hasImages: hasImages(month, slug)
    };
  }).sort((a, b) => a.id - b.id);
}
function getPostsForMonth(month) {
  return getPostSlugsForMonth(month).map((slug) => {
    const raw = readFileSync(join(BASE, month, `${slug}.md`), "utf-8");
    const { data, content } = matter(fixFrontmatter(raw));
    return {
      slug,
      month,
      date: slugToDate(slug),
      datetime: String(data.date),
      id: Number(data.id),
      preview: textPreview(content),
      commentCount: countComments(month, slug),
      hasImages: hasImages(month, slug)
    };
  });
}
function getImageFiles(month, slug) {
  const dir = join(BASE, month, `${slug}.files`);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => /\.(jpg|jpeg|png|gif|webp)$/i.test(f)).map((f) => `${REPO_BASE}/${month}/${slug}.files/${f}`);
}
function getCommentImages(month, slug, commentFileBase) {
  const dir = join(BASE, month, `${slug}.comments`);
  if (!existsSync(dir)) return [];
  const commentId = commentFileBase.split("-")[0];
  const prefix = commentId + "-";
  return readdirSync(dir).filter((f) => f.startsWith(prefix) && /\.(jpg|jpeg|png|gif|webp)$/i.test(f)).map((f) => `${REPO_BASE}/${month}/${slug}.comments/${f}`);
}
function getPost(month, slug) {
  const raw = readFileSync(join(BASE, month, `${slug}.md`), "utf-8");
  const { data, content } = matter(fixFrontmatter(raw));
  const commentsDir = join(BASE, month, `${slug}.comments`);
  const comments = [];
  if (existsSync(commentsDir)) {
    const commentFiles = readdirSync(commentsDir).filter((f) => f.endsWith(".md")).sort((a, b) => {
      const idA = parseInt(a.split("-")[0], 10);
      const idB = parseInt(b.split("-")[0], 10);
      return idA - idB;
    });
    for (const cf of commentFiles) {
      const craw = readFileSync(join(commentsDir, cf), "utf-8");
      const { data: cd, content: cc } = matter(fixFrontmatter(craw));
      const fileBase = basename(cf, ".md");
      comments.push({
        id: Number(cd.id),
        date: String(cd.date),
        author: String(cd.author ?? "unknown"),
        authorHandle: cd.author_handle ? String(cd.author_handle) : void 0,
        bodyHtml: renderMarkdown(cc),
        images: getCommentImages(month, slug, fileBase),
        _replyToId: cd.reply_to ? Number(cd.reply_to) : void 0,
        _replyQuote: cd.reply_quote ? String(cd.reply_quote) : void 0
      });
    }
  }
  const byId = new Map(comments.map((c) => [c.id, c]));
  for (const c of comments) {
    if (c._replyToId) {
      const explicitQuote = c._replyQuote;
      const ref = byId.get(c._replyToId);
      c.replyTo = {
        author: ref?.author ?? "…",
        // prefer the exact selected quote; fall back to first 160 chars of the referenced message
        preview: explicitQuote ?? (ref?.bodyHtml.replace(/<[^>]+>/g, "").trim().slice(0, 160) ?? "")
      };
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
    comments
  };
}

function buildSidebarProps(currentMonth) {
  const months = getMonths();
  const postsIndex = {};
  postsIndex[currentMonth] = getPostsForMonth(currentMonth);
  return { sidebarMonths: months, currentMonth, postsIndex };
}

export { $$Layout as $, getMonths as a, buildSidebarProps as b, getPostSlugsForMonth as c, getPostsForDay as d, getAllDays as e, getPostsForMonth as f, getPost as g };
