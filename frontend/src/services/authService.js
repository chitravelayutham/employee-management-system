//Contains my APIs for authentication and authorization

import axios from 'axios'

export const loginUser = async (username, password) => {
  const response = await axios.post('/login', {
    username,
    password,
  })
  return response.data
}