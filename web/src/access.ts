/**
 * @see https://umijs.org/zh-CN/plugins/plugin-access
 * */
export default function access(initialState: { currentUser?: API.CurrentUser } | undefined) {
  const { currentUser } = initialState ?? {};
  return {
    canGuest: currentUser && currentUser.access.includes("guest"),
    canAdmin: currentUser && currentUser.access.includes("admin"),
  };
}
