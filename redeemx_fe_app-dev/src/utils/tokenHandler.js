export const getToken = () => localStorage.getItem('token');
export const getUserRole = () => ({
  is_user: localStorage.getItem('is_user') === 'true',
  is_admin: localStorage.getItem('is_admin') === 'true',
  is_vendor: localStorage.getItem('is_vendor') === 'true',
});

export const removeToken = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('is_user');
  localStorage.removeItem('is_admin');
  localStorage.removeItem('is_vendor');
};
