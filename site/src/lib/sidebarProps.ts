import { getMonths, getPostSlugsForMonth, getPostsForMonth } from './posts';

export function buildSidebarProps(currentMonth: string, currentDay?: string) {
  const months = getMonths();
  const postsIndex: Record<string, ReturnType<typeof getPostsForMonth>> = {};
  postsIndex[currentMonth] = getPostsForMonth(currentMonth);

  // First slug filename date per month (fast — just directory listing)
  const firstDayByMonth: Record<string, string> = {};
  for (const m of months) {
    const slugs = getPostSlugsForMonth(m);
    if (slugs.length > 0) firstDayByMonth[m] = slugs[0].slice(0, 10);
  }

  return { sidebarMonths: months, currentMonth, currentDay: currentDay ?? '', postsIndex, firstDayByMonth };
}
