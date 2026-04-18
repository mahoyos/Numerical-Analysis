import { beforeEach, describe, expect, it, vi } from 'vitest';

import { DownloadChartUtils } from '../../../src/util/DownloadChartUtils';

describe('DownloadChartUtils', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('returns early when canvas is null', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => undefined);

    await DownloadChartUtils.downloadSVG(null);

    expect(errorSpy).toHaveBeenCalled();
  });

  it('downloads an svg file from canvas', async () => {
    const canvas = document.createElement('canvas');
    Object.defineProperty(canvas, 'width', { value: 400 });
    Object.defineProperty(canvas, 'height', { value: 300 });

    const contextMock = {} as CanvasRenderingContext2D;
    vi.spyOn(canvas, 'getContext').mockReturnValue(contextMock);
    vi.spyOn(canvas, 'toDataURL').mockReturnValue('data:image/png;base64,AA==');

    const clickSpy = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => undefined);

    if (!('createObjectURL' in URL)) {
      Object.defineProperty(URL, 'createObjectURL', {
        value: () => 'blob:mock-url',
        writable: true,
      });
    }
    if (!('revokeObjectURL' in URL)) {
      Object.defineProperty(URL, 'revokeObjectURL', {
        value: () => undefined,
        writable: true,
      });
    }

    const appendSpy = vi.spyOn(document.body, 'appendChild');
    const removeSpy = vi.spyOn(document.body, 'removeChild');
    const objectUrlSpy = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:mock-url');
    const revokeSpy = vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => undefined);

    await DownloadChartUtils.downloadSVG(canvas, 'chart.svg');

    expect(objectUrlSpy).toHaveBeenCalled();
    expect(clickSpy).toHaveBeenCalledTimes(1);
    expect(appendSpy).toHaveBeenCalled();
    expect(removeSpy).toHaveBeenCalled();
    expect(revokeSpy).toHaveBeenCalledWith('blob:mock-url');
  });

  it('throws when canvas has no 2D context', async () => {
    const canvas = document.createElement('canvas');
    vi.spyOn(canvas, 'getContext').mockReturnValue(null);

    await expect(DownloadChartUtils.downloadSVG(canvas)).rejects.toThrow(
      'Could not get 2D context from canvas',
    );
  });
});
