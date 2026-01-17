import React from 'react';

interface ContactUsConfirmationProps {
  success: boolean;
  message: string;
}

const ContactUsConfirmation: React.FC<ContactUsConfirmationProps> = ({ success, message }) => {
  return (
    <div className={`alert ${success ? 'alert-success' : 'alert-error'}`}>
      {message}
    </div>
  );
};

export default ContactUsConfirmation;
