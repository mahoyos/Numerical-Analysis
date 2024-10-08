import axios from 'axios';

const API_URL: string = import.meta.env.VITE_API_URL as string;

class NonLinearEquationsService {

  async postFixedPointData(formData: any): Promise<any> {
    try {
      const response = await axios.post(API_URL + 'fixed-point', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error posting data:', error);
      throw error;
    }
  }

  async postFalsePositionData(formData: any): Promise<any> {
    try {
      const response = await axios.post(API_URL + 'false-position', formData, {
        headers: {
          'Content-Type': 'application/json' 
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error posting data:', error);
      throw error;
    }
  }
}

export default new NonLinearEquationsService();
