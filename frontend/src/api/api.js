import axios from "axios"


// Replace <EC2_PUBLIC_IP> with the Terraform output public IP
//const EC2_PUBLIC_IP = "3.80.136.36"; // e.g., 3.91.68.245

//export const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";
/* const API = axios.create({
    baseURL: BASE_URL,
})
 */

const API = axios.create({
  baseURL: process.env.VITE_API_URL || "http://localhost:8080",
  headers: {
    "Content-Type": "application/json",
  },
});


API.interceptors.request.use((req) => {
    const token = localStorage.getItem("access_token")
    if (token) {
        req.headers.Authorization = `Bearer ${token}`
    }
    return req
})

export default API