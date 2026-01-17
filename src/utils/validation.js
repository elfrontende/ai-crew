export const validateName = (name) => {
  if (!name) return "Name is required.";
  if (name.length < 2) return "Name must be at least 2 characters.";
  return null;
};

export const validateEmail = (email) => {
  if (!email) return "Email is required.";
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) return "Email is not valid.";
  return null;
};

export const validateMessage = (message) => {
  if (!message) return "Message is required.";
  if (message.length < 10) return "Message must be at least 10 characters.";
  return null;
};
