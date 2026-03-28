import axios from "axios"


export const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";
const API = axios.create({
    baseURL: BASE_URL,
})

API.interceptors.request.use((req) => {
    const token = localStorage.getItem("access_token")
    if (token) {
        req.headers.Authorization = `Bearer ${token}`
    }
    return req
})

export default API