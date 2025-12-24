import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/', // Replace with your API base URL

});

export default apiClient;