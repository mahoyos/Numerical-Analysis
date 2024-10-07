export class DownloadChartUtils {
    static async downloadSVG(chartElement: HTMLCanvasElement | null, fileName: string = 'chart.svg'): Promise<void> {
        if (!chartElement) {
            console.error('Chart element not found');
            return;
        }

        const svgString = DownloadChartUtils.convertCanvasToSVG(chartElement);
        const svgBlob = new Blob([svgString], {type: 'image/svg+xml;charset=utf-8'});
        const svgUrl = URL.createObjectURL(svgBlob);
        
        const downloadLink = document.createElement('a');
        downloadLink.href = svgUrl;
        downloadLink.download = fileName;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        URL.revokeObjectURL(svgUrl);
    }

    private static convertCanvasToSVG(canvas: HTMLCanvasElement): string {
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            throw new Error('Could not get 2D context from canvas');
        }

        const svgNamespace = "http://www.w3.org/2000/svg";
        const svgElement = document.createElementNS(svgNamespace, "svg");
        svgElement.setAttribute("width", canvas.width.toString());
        svgElement.setAttribute("height", canvas.height.toString());

        const svgImg = document.createElementNS(svgNamespace, "image");
        svgImg.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", canvas.toDataURL("image/png"));
        svgImg.setAttribute("width", canvas.width.toString());
        svgImg.setAttribute("height", canvas.height.toString());

        svgElement.appendChild(svgImg);

        const svgString = new XMLSerializer().serializeToString(svgElement);
        return svgString;
    }
}