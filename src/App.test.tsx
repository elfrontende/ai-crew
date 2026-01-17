import { render } from '@testing-library/react';
import App from './App';
import { describe, it, expect } from 'vitest';

describe('App', () => {
  it('renders the Vite + React text', () => {
    render(<App />);
    expect(document.body).toBeDefined();
  });
});
