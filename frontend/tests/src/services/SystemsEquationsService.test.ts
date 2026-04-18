import { describe, expect, it, vi, beforeEach } from 'vitest';
import axios from 'axios';

import SystemsEquationsService from '../../../src/services/SystemsEquationsService';

vi.mock('axios');
const mockedAxios = vi.mocked(axios);

describe('SystemsEquationsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('posts systems equations data successfully', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { status: 'success' } } as never);

    const response = await SystemsEquationsService.postSystemsEquationsData({ method: 'jacobi' });

    expect(mockedAxios.post).toHaveBeenCalledTimes(1);
    expect(response.status).toBe('success');
  });

  it('throws when systems equations request fails', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('systems error'));

    await expect(SystemsEquationsService.postSystemsEquationsData({ method: 'jacobi' })).rejects.toThrow(
      'systems error',
    );
  });
});
