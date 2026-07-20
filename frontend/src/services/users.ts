import apiClient from './api';

export interface RegisterUserRequest {
  first_name: string
  last_name: string
  email: string
  password: string
}

export interface CreatedUser {
  id: string;
  first_name: string
  last_name: string
  email: string
  role: string
}

export interface RegisterUserResponse {
  detail?: string;
  user?: CreatedUser;
}

export interface ApiValidationErrors {
  [field: string]: string |string[];
}

export async function registerUser(userData: RegisterUserRequest): Promise<RegisterUserResponse> {
  const response = await apiClient.post('accounts/register/', userData);

  return response.data;
}