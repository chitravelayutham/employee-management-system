//Contains my APIs for authentication and authorization

import axios from 'axios'

export const loginUser = async (email, password) => {
  const response = await axios.post('/login', {
    email,
    password,
  })
  return response.data
}