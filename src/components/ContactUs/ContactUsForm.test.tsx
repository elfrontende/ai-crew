import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ContactUsForm from './ContactUsForm';

describe('ContactUsForm', () => {
  it('should display validation errors for empty fields', async () => {
    render(<ContactUsForm />);

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(await screen.findByText(/name is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/message is required/i)).toBeInTheDocument();
  });

  it('should display an error for invalid email', async () => {
    render(<ContactUsForm />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'invalid-email' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(await screen.findByText(/email is not valid/i)).toBeInTheDocument();
  });

  it('should submit the form when all fields are valid', async () => {
    const handleSubmit = vi.fn();
    render(<ContactUsForm onSubmit={handleSubmit} />);

    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'john.doe@example.com' } });
    fireEvent.change(screen.getByLabelText(/message/i), { target: { value: 'This is a valid message.' } });

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(handleSubmit).toHaveBeenCalled();
  });
});
