import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import CertificationsSection from '../CertificationsSection';
import * as api from '../../services/api';

// Mock the API
vi.mock('../../services/api', () => ({
  certificationsApi: {
    getAll: vi.fn(),
  },
}));

const mockCertifications = [
  {
    id: 'aws-saa-c03',
    name: 'AWS Solutions Architect Associate',
    provider: 'AWS',
    issue_date: '2024-01-15',
    expiry_date: '2027-01-15',
    credential_id: 'ABC123',
    computed_status: 'active' as const,
  },
  {
    id: 'azure-az-900',
    name: 'Azure Fundamentals',
    provider: 'Azure',
    issue_date: '2023-06-01',
    expiry_date: '2024-01-01',
    credential_id: 'XYZ789',
    computed_status: 'expired' as const,
  },
  {
    id: 'gcp-ace',
    name: 'Google Cloud Associate Cloud Engineer',
    provider: 'GCP',
    issue_date: '2024-03-01',
    expiry_date: '2025-02-01',
    credential_id: 'GCP456',
    computed_status: 'expiring_soon' as const,
  },
];

const renderWithQueryClient = (component: React.ReactElement) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

describe('CertificationsSection', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it('displays loading state initially', () => {
    vi.mocked(api.certificationsApi.getAll).mockImplementation(() => new Promise(() => {}));
    
    renderWithQueryClient(<CertificationsSection />);
    
    expect(screen.getByText('Loading certifications...')).toBeInTheDocument();
  });

  it('displays certifications with various expiry states', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: mockCertifications,
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByText('AWS Solutions Architect Associate')).toBeInTheDocument();
    });

    // Test active certification
    expect(screen.getByText('Active')).toBeInTheDocument();
    
    // Test expired certification
    expect(screen.getByText('Expired')).toBeInTheDocument();
    
    // Test expiring soon certification
    expect(screen.getByText('Expiring Soon')).toBeInTheDocument();

    // Test provider display
    expect(screen.getByText('AWS')).toBeInTheDocument();
    expect(screen.getByText('Azure')).toBeInTheDocument();
    expect(screen.getByText('GCP')).toBeInTheDocument();

    // Test credential IDs
    expect(screen.getByText('ABC123')).toBeInTheDocument();
    expect(screen.getByText('XYZ789')).toBeInTheDocument();
    expect(screen.getByText('GCP456')).toBeInTheDocument();
  });

  it('filters certifications by provider', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: mockCertifications.filter(cert => cert.provider === 'AWS'),
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByDisplayValue('all')).toBeInTheDocument();
    });

    // Change provider filter to AWS
    const providerSelect = screen.getByDisplayValue('all');
    fireEvent.change(providerSelect, { target: { value: 'AWS' } });

    await waitFor(() => {
      expect(api.certificationsApi.getAll).toHaveBeenCalledWith({ provider: 'AWS' });
    });
  });

  it('filters certifications by status', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: mockCertifications.filter(cert => cert.computed_status === 'active'),
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getAllByDisplayValue('all')).toHaveLength(2); // provider and status filters
    });

    // Change status filter to active
    const statusSelects = screen.getAllByDisplayValue('all');
    const statusSelect = statusSelects[1]; // Second select is status filter
    fireEvent.change(statusSelect, { target: { value: 'active' } });

    await waitFor(() => {
      expect(api.certificationsApi.getAll).toHaveBeenCalledWith({ status: 'active' });
    });
  });

  it('filters certifications by search query', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: mockCertifications,
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByText('AWS Solutions Architect Associate')).toBeInTheDocument();
    });

    // Search for "AWS"
    const searchInput = screen.getByPlaceholderText('Search certifications...');
    fireEvent.change(searchInput, { target: { value: 'AWS' } });

    // Should show only AWS certification in the results count
    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument();
      expect(screen.getByText('certifications matching your query')).toBeInTheDocument();
    });

    // AWS certification should still be visible
    expect(screen.getByText('AWS Solutions Architect Associate')).toBeInTheDocument();
    
    // Azure and GCP certifications should not be visible in filtered results
    expect(screen.queryByText('Azure Fundamentals')).not.toBeInTheDocument();
    expect(screen.queryByText('Google Cloud Associate Cloud Engineer')).not.toBeInTheDocument();
  });

  it('handles API failures gracefully', async () => {
    vi.mocked(api.certificationsApi.getAll).mockRejectedValue(new Error('API Error'));

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load certifications')).toBeInTheDocument();
    });

    // Should not show loading state
    expect(screen.queryByText('Loading certifications...')).not.toBeInTheDocument();
    
    // Should not show any certifications
    expect(screen.queryByText('AWS Solutions Architect Associate')).not.toBeInTheDocument();
  });

  it('displays empty state when no certifications match criteria', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: [],
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByText('No certifications found matching your criteria.')).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText('0')).toBeInTheDocument();
      expect(screen.getByText('certifications matching your query')).toBeInTheDocument();
    });
  });

  it('formats dates correctly', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: [mockCertifications[0]], // AWS cert with dates
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByText('AWS Solutions Architect Associate')).toBeInTheDocument();
    });

    // Check formatted dates (Jan 15, 2024 and Jan 15, 2027)
    expect(screen.getByText('Jan 15, 2024')).toBeInTheDocument();
    expect(screen.getByText('Jan 15, 2027')).toBeInTheDocument();
  });

  it('updates query string display when filters change', async () => {
    vi.mocked(api.certificationsApi.getAll).mockResolvedValue({
      certifications: mockCertifications,
    });

    renderWithQueryClient(<CertificationsSection />);

    await waitFor(() => {
      expect(screen.getByText('GET')).toBeInTheDocument();
      expect(screen.getByText('/certifications')).toBeInTheDocument();
    });

    // Initial query should show default filters
    expect(screen.getByText('?provider=all&status=all')).toBeInTheDocument();

    // Change provider filter
    const providerSelect = screen.getByDisplayValue('all');
    fireEvent.change(providerSelect, { target: { value: 'AWS' } });

    // Query string should update
    await waitFor(() => {
      expect(screen.getByText('?provider=AWS&status=all')).toBeInTheDocument();
    });
  });
});