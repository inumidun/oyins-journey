import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import APIExplorer from '../APIExplorer';
import * as api from '../../services/api';

// Mock the API
vi.mock('../../services/api', () => ({
  default: {
    get: vi.fn(),
  },
}));

// Mock environment variable
Object.defineProperty(import.meta, 'env', {
  value: {
    VITE_API_URL: 'https://api.test.dev',
  },
  writable: true,
});

describe('APIExplorer', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it('renders API explorer with endpoints', () => {
    render(<APIExplorer />);
    
    // Verify the main heading is displayed
    expect(screen.getByText('Your CV as an')).toBeInTheDocument();
    expect(screen.getByText('API')).toBeInTheDocument();
    
    // Verify endpoints are listed
    expect(screen.getAllByText('/skills').length).toBeGreaterThan(0);
    expect(screen.getAllByText('/projects').length).toBeGreaterThan(0);
    expect(screen.getAllByText('/certifications').length).toBeGreaterThan(0);
    expect(screen.getAllByText('/adrs').length).toBeGreaterThan(0);
    expect(screen.getAllByText('/health').length).toBeGreaterThan(0);
  });

  it('displays endpoint details when selected', () => {
    render(<APIExplorer />);
    
    // Click on skills endpoint
    const skillsButtons = screen.getAllByText('/skills');
    fireEvent.click(skillsButtons[0]);
    
    // Verify description is shown
    expect(screen.getByText('List all skills with optional filtering')).toBeInTheDocument();
    
    // Verify parameters section exists
    expect(screen.getByText('Query Parameters:')).toBeInTheDocument();
  });

  it('shows try it button and handles API calls', async () => {
    const mockResponse = { data: { test: 'data' } };
    vi.mocked(api.default.get).mockResolvedValue(mockResponse);

    render(<APIExplorer />);
    
    // Select skills endpoint
    const skillsButtons = screen.getAllByText('/skills');
    fireEvent.click(skillsButtons[0]);
    
    // Find and click try it button
    const tryItButton = screen.getByText('Try it');
    expect(tryItButton).toBeInTheDocument();
    
    fireEvent.click(tryItButton);
    
    // Wait for API call to complete
    await waitFor(() => {
      expect(api.default.get).toHaveBeenCalledWith('/skills');
    });
  });

  it('handles API errors gracefully', async () => {
    const mockError = new Error('API Error');
    (mockError as any).response = { status: 500 };
    vi.mocked(api.default.get).mockRejectedValue(mockError);

    render(<APIExplorer />);
    
    // Select skills endpoint
    const skillsButtons = screen.getAllByText('/skills');
    fireEvent.click(skillsButtons[0]);
    
    // Execute API call
    const tryItButton = screen.getByText('Try it');
    fireEvent.click(tryItButton);
    
    // Wait for error handling
    await waitFor(() => {
      expect(api.default.get).toHaveBeenCalledWith('/skills');
    });
  });

  it('displays no parameters message for endpoints without params', () => {
    render(<APIExplorer />);
    
    // Select health endpoint (has no parameters)
    const healthButtons = screen.getAllByText('/health');
    fireEvent.click(healthButtons[0]);
    
    // Verify description is shown
    expect(screen.getByText('System health status')).toBeInTheDocument();
    
    // Verify no parameters message
    expect(screen.getByText('No parameters required')).toBeInTheDocument();
  });
});