import axios, { AxiosError } from "axios";
import router from "../../router";

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

//overwites the current cookies with a new set of cookies
export const setCookies = (cookies: Record<string, string>) => {
  if (Object.keys(cookies).length == 0) {
    document.cookie = "";
    return;
  }
  const string: string = Object.keys(cookies).reduce(
    (prev: string, item: string) => {
      prev += item + "=" + cookies[item] + "; ";
      return prev;
    }
  );
  document.cookie = string;
};

export const deleteCookie = (name: string) => {
  document.cookie = name + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
};

export const getAccount = async () => {
  try {
    const response = await axios.get("http://localhost:5000/accounts", {
      withCredentials: true,
    });
    return response.data;
  } catch (err: AxiosError | any) {
    const cookies = getCookies();
    console.log(cookies);
    delete cookies["session_id"];
    console.log(cookies);
    setCookies(cookies);
    deleteCookie("session_id");
    router.push("/login?error");
  }
};
