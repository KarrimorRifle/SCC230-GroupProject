export const getCookies = () => {
  const cookies: string = document.cookie;
  let returnValue: Record<string, string> = {};
  cookies.split("; ").forEach((item: string) => {
    const temp: Record<string, string> = {};
    temp[item.split("=")[0]] = item.split("=")[1];
    if (Object.keys(returnValue).length == 0) returnValue = { ...temp };
    returnValue = { ...returnValue, ...temp };
  });
  return returnValue;
};
