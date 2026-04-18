import { describe, expect, it, vi, beforeEach } from 'vitest';
import axios from 'axios';

import InterpolationsService from '../../../src/services/InterpolationsService';

vi.mock('axios');
const mockedAxios = vi.mocked(axios);

describe('InterpolationsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('posts interpolation data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { polynom: 'x + 1' } } as never);

    const response = await InterpolationsService.postInterpolationsData({ method: 'newton' });

    expect(mockedAxios.post).toHaveBeenCalledTimes(1);
    expect(response.polynom).toBe('x + 1');
  });

  it('throws when interpolation request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('request failed'));

    await expect(InterpolationsService.postInterpolationsData({ method: 'newton' })).rejects.toThrow(
      'request failed',
    );
  });
});
