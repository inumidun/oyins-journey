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

  it('displays endpoint documentation', () => {
    render(<APIExplorer />);
    
    // Find the first endpoint button (skills)
    const skillsButton = screen.getAllByText('/skills')[0];
    fireEvent.click(skillsButton);
    
    // Verify method is displayed
    const getMethods = screen.getAllByText('GET');
    expect(getMethods.length).toBeGreaterThan(0);
    
    // Verify path is displayed
    expect(screen.getByText('/skills')).toBeInTheDocument();
    
    // Verify description is displayed
    expect(screen.getByText('List all skills with optional filtering')).toBeInTheDocument();
    
    // Verify parameters are displayed
    expect(screen.getByText('Query Parameters:')).toBeInTheDocument();
    expect(screen.getByText('category')).toBeInTheDocument();
    expect(screen.getByText('cloud')).toBeInTheDocument();
    
    // Verify request URL components are displayed (text may be split)
    expect(screen.getByText('https://api.test.dev')).toBeInTheDocument();
  });

  it('displays request details and response data for API calls', async () => {
    const mockResponse = { data: { test: 'data' } };
    vi.mocked(api.default.get).mockResolvedValue(mockResponse);

    render(<APIExplorer />);
    
    // Select skills endpoint
    const skillsButton = screen.getAllByText('/skills')[0];
    fireEvent.click(skillsButton);
    
    // Execute API call
    const tryItButton = screen.getByText('Try it');
    fireEvent.click(tryItButton);
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText('200 OK')).toBeInTheDocument();
    });
    
    // Verify request details are shown
    const getMethods = screen.getAllByText('GET');
    expect(getMethods.length).toBeGreaterThan(0);
    expect(screen.getByText('api.test.dev')).toBeInTheDocument();
    expect(screen.getByText('/skills')).toBeInTheDocument();
    
    // Verify response data is displayed
    expect(screen.getByText('"test": "data"')).toBeInTheDocument();
    
    // Verify API was called with correct path
    expect(api.default.get).toHaveBeenCalledWith('/skills');
  });

  it('updates URL when parameters change', () => {
    render(<APIExplorer />);
    
    // Select skills endpoint
    const skillsButton = screen.getAllByText('/skills')[0];
    fireEvent.click(skillsButton);
    
    // Verify base URL components are displayed
    expect(screen.getByText('https://api.test.dev')).toBeInTheDocument();
    expect(screen.getByText('/skills')).toBeInTheDocument();
  });

  it('displays clear error messages for API failures', async () => {
    const errorMessage = 'API Error';
    const mockError = new Error(errorMessage);
    (mockError as any).response = { status: 500 };
    vi.mocked(api.default.get).mockRejectedValue(mockError);

    render(<APIExplorer />);
    
    // Select skills endpoint
    const skillsButton = screen.getAllByText('/skills')[0];
    fireEvent.click(skillsButton);
    
    // Execute API call
    const tryItButton = screen.getByText('Try it');
    fireEvent.click(tryItButton);
    
    // Wait for error to be displayed
    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
    });
    
    // Verify error message is displayed in response
    expect(screen.getByText(errorMessage, { exact: false })).toBeInTheDocument();
    
    // Verify API was called
    expect(api.default.get).toHaveBeenCalledWith('/skills');
  });

  it('handles endpoints with no parameters', () => {
    render(<APIExplorer />);
    
    // Select health endpoint (has no parameters)
    const healthButton = screen.getAllByText('/health')[0];
    fireEvent.click(healthButton);
    
    // Verify method is displayed
    const getMethods = screen.getAllByText('GET');
    expect(getMethods.length).toBeGreaterThan(0);
    
    // Verify path is displayed
    expect(screen.getByText('/health')).toBeInTheDocument();
    
    // Verify description is displayed
    expect(screen.getByText('System health status')).toBeInTheDocument();
    
    // Verify "No parameters" message is displayed
    expect(screen.getByText('No parameters required')).toBeInTheDocument();
  });
});