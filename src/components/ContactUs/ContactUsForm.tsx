import React from 'react';
import { useForm } from 'react-hook-form';
import create from 'zustand';
import { devtools } from 'zustand/middleware';

interface ContactFormState {
  name: string;
  email: string;
  subject: string;
  message: string;
  setName: (name: string) => void;
  setEmail: (email: string) => void;
  setMessage: (message: string) => void;
}

const useContactFormStore = create<ContactFormState>()(
  devtools((set) => ({
    name: '',
    email: '',
    subject: '',
    message: '',
    setName: (name) => set({ name }),
    setEmail: (email) => set({ email }),
    setSubject: (subject) => set({ subject }),
    setMessage: (message) => set({ message }),
  }))
);

const ContactUsForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      name: '',
      email: '',
      message: '',
    }
  });
  const { name, email, subject, message, setName, setEmail, setSubject, setMessage } = useContactFormStore();

  const onSubmit = (data: any) => {
    // Here you can handle the form submission, e.g., send data to an API
    console.log('Form submitted:', data);
    // Reset form fields after submission
    setName('');
    setEmail('');
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-lg mx-auto p-4 bg-white shadow-md rounded">
      <div className="mb-4">
        <label htmlFor="subject" className="block text-sm font-medium text-gray-700">Subject</label>
        <input
          id="subject"
          type="text"
          {...register('subject', { required: 'Subject is required' })}
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        {errors.subject && <p className="mt-2 text-sm text-red-600">{errors.subject.message}</p>}
      </div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
        <input
          id="name"
          type="text"
          {...register('name', { required: 'Name is required' })}
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        {errors.name && <p className="mt-2 text-sm text-red-600">{errors.name.message}</p>}
      </div>

      <div className="mb-4">
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
        <input
          id="email"
          type="email"
          {...register('email', { required: 'Email is required', pattern: { value: /^\S+@\S+$/i, message: 'Invalid email address' } })}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        {errors.email && <p className="mt-2 text-sm text-red-600">{errors.email.message}</p>}
      </div>

      <div className="mb-4">
        <label htmlFor="message" className="block text-sm font-medium text-gray-700">Message</label>
        <textarea
          id="message"
          {...register('message', { required: 'Message is required' })}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        {errors.message && <p className="mt-2 text-sm text-red-600">{errors.message.message}</p>}
      </div>

      <button type="submit" className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
        Submit
      </button>
    </form>
  );
};

export default ContactUsForm;
