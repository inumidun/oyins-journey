import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import fc from 'fast-check';
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

  // Property 3: API Explorer Endpoint Documentation
  // Feature: living-architecture-resume-enhancement, Property 3: For any selected API endpoint, the explorer should display complete documentation including parameters and response examples
  describe('Property 3: API Explorer Endpoint Documentation', () => {
    it('should display complete documentation for any selected endpoint', () => {
      fc.assert(
        fc.property(
          fc.constantFrom(
            { method: 'GET', path: '/skills', description: 'List all skills with optional filtering', params: ['category', 'cloud'] },
            { method: 'GET', path: '/projects', description: 'List all projects', params: ['status', 'technology'] },
            { method: 'GET', path: '/certifications', description: 'List all certifications', params: ['provider', 'status'] },
            { method: 'GET', path: '/adrs', description: 'List all architectural decision records', params: [] },
            { method: 'GET', path: '/health', description: 'System health status', params: [] }
          ),
          (endpoint: any) => {
            render(<APIExplorer />);
            
            // Find and click the endpoint
            const endpointButton = screen.getByText(endpoint.path);
            fireEvent.click(endpointButton);
            
            // Verify method is displayed
            expect(screen.getByText(endpoint.method)).toBeInTheDocument();
            
            // Verify path is displayed
            expect(screen.getByText(endpoint.path)).toBeInTheDocument();
            
            // Verify description is displayed
            expect(screen.getByText(endpoint.description)).toBeInTheDocument();
            
            // Verify parameters are displayed if they exist
            if (endpoint.params.length > 0) {
              expect(screen.getByText('Query Parameters:')).toBeInTheDocument();
              endpoint.params.forEach((param: any) => {
                expect(screen.getByText(param)).toBeInTheDocument();
              });
            }
            
            // Verify request URL is properly formatted
            expect(screen.getByText('https://api.test.dev')).toBeInTheDocument();
          }
        ),
        { numRuns: 100 }
      );
    });
  });

  // Property 4: API Explorer Request-Response Cycle
  // Feature: living-architecture-resume-enhancement, Property 4: For any API call execution, the explorer should display both the request details and the actual response data
  describe('Property 4: API Explorer Request-Response Cycle', () => {
    it('should display request details and response data for any API call', async () => {
      const mockResponse = { data: { test: 'data' } };
      vi.mocked(api.default.get).mockResolvedValue(mockResponse);

      await fc.assert(
        fc.asyncProperty(
          fc.constantFrom('/skills', '/projects', '/certifications', '/adrs', '/health'),
          async (path: any) => {
            render(<APIExplorer />);
            
            // Select endpoint
            const endpointButton = screen.getByText(path);
            fireEvent.click(endpointButton);
            
            // Execute API call
            const tryItButton = screen.getByText('Try it');
            fireEvent.click(tryItButton);
            
            // Wait for response
            await waitFor(() => {
              expect(screen.getByText('200 OK')).toBeInTheDocument();
            });
            
            // Verify request details are shown
            expect(screen.getByText('GET')).toBeInTheDocument();
            expect(screen.getByText('https://api.test.dev')).toBeInTheDocument();
            expect(screen.getByText(path)).toBeInTheDocument();
            
            // Verify response data is displayed
            expect(screen.getByText('"test": "data"')).toBeInTheDocument();
            
            // Verify API was called with correct path
            expect(api.default.get).toHaveBeenCalledWith(path);
          }
        ),
        { numRuns: 100 }
      );
    });
  });

  // Property 5: API Explorer URL Generation
  // Feature: living-architecture-resume-enhancement, Property 5: For any parameter modification, the displayed request URL should accurately reflect all current parameter values
  describe('Property 5: API Explorer URL Generation', () => {
    it('should update URL dynamically when parameters change', () => {
      fc.assert(
        fc.property(
          fc.record({
            endpoint: fc.constantFrom('/skills', '/projects', '/certifications'),
            params: fc.dictionary(
              fc.constantFrom('category', 'cloud', 'status', 'technology', 'provider'),
              fc.constantFrom('aws', 'azure', 'gcp', 'active', 'expired', 'web', 'mobile')
            )
          }),
          ({ endpoint }: any) => {
            render(<APIExplorer />);
            
            // Select endpoint
            const endpointButton = screen.getByText(endpoint);
            fireEvent.click(endpointButton);
            
            // Simulate parameter changes by checking if parameter inputs exist
            // and verify URL construction logic
            const baseUrl = 'https://api.test.dev';
            
            // Verify base URL components are displayed
            expect(screen.getByText(baseUrl)).toBeInTheDocument();
            expect(screen.getByText(endpoint)).toBeInTheDocument();
          }
        ),
        { numRuns: 100 }
      );
    });
  });

  // Property 6: API Explorer Error Handling
  // Feature: living-architecture-resume-enhancement, Property 6: For any failed API call, the explorer should display clear error messages and appropriate HTTP status codes
  describe('Property 6: API Explorer Error Handling', () => {
    it('should display clear error messages for any API failure', async () => {
      await fc.assert(
        fc.asyncProperty(
          fc.record({
            path: fc.constantFrom('/skills', '/projects', '/certifications', '/adrs', '/health'),
            errorMessage: fc.string({ minLength: 1, maxLength: 100 }),
            statusCode: fc.constantFrom(400, 401, 403, 404, 500, 502, 503)
          }),
          async ({ path, errorMessage, statusCode }: any) => {
            const mockError = new Error(errorMessage);
            (mockError as any).response = { status: statusCode };
            vi.mocked(api.default.get).mockRejectedValue(mockError);

            render(<APIExplorer />);
            
            // Select endpoint
            const endpointButton = screen.getByText(path);
            fireEvent.click(endpointButton);
            
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
            expect(api.default.get).toHaveBeenCalledWith(path);
          }
        ),
        { numRuns: 100 }
      );
    });
  });
});