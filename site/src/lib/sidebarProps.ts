import { getMonths, getPostsForMonth } from './posts';

export function buildSidebarProps() {
  const months = getMonths();
  const calendarMonths = months.slice(-2).reverse(); // last 2 months
  const postsIndex: Record<string, ReturnType<typeof getPostsForMonth>> = {};
  for (const m of calendarMonths) {
    postsIndex[m] = getPostsForMonth(m);
  }
  return { sidebarMonths: months, calendarMonths, postsIndex };
}
