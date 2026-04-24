import { getMonths, getPostsForMonth } from './posts';

export function buildSidebarProps(currentMonth: string) {
  const months = getMonths();
  const postsIndex: Record<string, ReturnType<typeof getPostsForMonth>> = {};
  postsIndex[currentMonth] = getPostsForMonth(currentMonth);
  return { sidebarMonths: months, currentMonth, postsIndex };
}
