import { describe, expect, it, vi, beforeEach } from 'vitest';
import axios from 'axios';

import NonLinearEquationsService from '../../../src/services/NonLinearEquationsService';

vi.mock('axios');

const mockedAxios = vi.mocked(axios);

describe('NonLinearEquationsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('posts bisection data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);

    const response = await NonLinearEquationsService.postBisectionData({ left_bound: 0, right_bound: 2 });

    expect(mockedAxios.post).toHaveBeenCalled();
    expect(response.status).toBe('success');
  });

  it('posts fixed point data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);
    const response = await NonLinearEquationsService.postFixedPointData({ initial_guess: 1 });
    expect(mockedAxios.post).toHaveBeenCalled();
    expect(response.status).toBe('success');
  });

  it('posts newton-raphson data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);
    const response = await NonLinearEquationsService.postNewtonRaphsonData({ initial_guess: 1 });
    expect(mockedAxios.post).toHaveBeenCalled();
    expect(response.status).toBe('success');
  });

  it('posts multiple roots data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);
    const response = await NonLinearEquationsService.postMultipleRootsData({ initial_guess: 1 });
    expect(mockedAxios.post).toHaveBeenCalled();
    expect(response.status).toBe('success');
  });

  it('posts false position data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);
    const response = await NonLinearEquationsService.postFalsePositionData({ left_bound: 0, right_bound: 2 });
    expect(mockedAxios.post).toHaveBeenCalled();
    expect(response.status).toBe('success');
  });

  it('posts secant data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);
    const response = await NonLinearEquationsService.postSecantData({ left_bound: 0, right_bound: 2 });
    expect(mockedAxios.post).toHaveBeenCalled();
    expect(response.status).toBe('success');
  });

  it('throws when request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('network'));

    await expect(
      NonLinearEquationsService.postSecantData({ left_bound: 0, right_bound: 2 }),
    ).rejects.toThrow('network');
  });

  it('throws when bisection request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('bisection error'));

    await expect(
      NonLinearEquationsService.postBisectionData({ left_bound: 0, right_bound: 2 }),
    ).rejects.toThrow('bisection error');
  });

  it('throws when fixed point request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('fixed point error'));

    await expect(NonLinearEquationsService.postFixedPointData({ initial_guess: 1 })).rejects.toThrow(
      'fixed point error',
    );
  });

  it('throws when newton-raphson request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('newton error'));

    await expect(NonLinearEquationsService.postNewtonRaphsonData({ initial_guess: 1 })).rejects.toThrow(
      'newton error',
    );
  });

  it('throws when multiple roots request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('multiple roots error'));

    await expect(NonLinearEquationsService.postMultipleRootsData({ initial_guess: 1 })).rejects.toThrow(
      'multiple roots error',
    );
  });

  it('throws when false position request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('false position error'));

    await expect(
      NonLinearEquationsService.postFalsePositionData({ left_bound: 0, right_bound: 2 }),
    ).rejects.toThrow('false position error');
  });
});
