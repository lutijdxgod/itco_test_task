export const saveToken = (token) => {
  localStorage.setItem("token", token);
};

export const saveUserID = (userID) => {
  localStorage.setItem("user_id", userID);
};

export const getToken = () => {
  return localStorage.getItem("token");
};

export const clearToken = () => {
  localStorage.removeItem("token");
};

export const isAuthenticated = () => {
  return !!getToken();
};
