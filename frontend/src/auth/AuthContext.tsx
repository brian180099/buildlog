import { createContext, useContext, useEffect, useMemo, useState } from 'react'

export type CurrentUser = {
  id: number
  email: string
  nickname: string
}

type AuthContextValue = {
  user: CurrentUser | null
  isLoading: boolean
  refresh: () => Promise<CurrentUser | null>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function getCurrentUser(): Promise<CurrentUser | null> {
  const response = await fetch(apiBaseUrl + '/api/auth/me', { credentials: 'include' })
  if (!response.ok) return null
  const result = (await response.json()) as { data: CurrentUser }
  return result.data
}

export async function submitAuthRequest(
  path: 'login' | 'register',
  payload: Record<string, string>,
): Promise<CurrentUser> {
  const response = await fetch(apiBaseUrl + '/api/auth/' + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  })
  const result = (await response.json()) as { data?: CurrentUser; detail?: string }
  if (!response.ok || !result.data) {
    throw new Error(result.detail ?? '요청을 처리하지 못했습니다.')
  }
  return result.data
}

export async function updateNickname(nickname: string): Promise<CurrentUser> {
  const response = await fetch(apiBaseUrl + '/api/auth/me', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ nickname }),
  })
  const result = (await response.json()) as { data?: CurrentUser; detail?: string }
  if (!response.ok || !result.data) {
    throw new Error(result.detail ?? '닉네임을 변경하지 못했습니다.')
  }
  return result.data
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const refresh = async () => {
    const nextUser = await getCurrentUser().catch(() => null)
    setUser(nextUser)
    setIsLoading(false)
    return nextUser
  }

  const logout = async () => {
    await fetch(apiBaseUrl + '/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    })
    setUser(null)
  }

  useEffect(() => {
    void refresh()
  }, [])

  const value = useMemo(() => ({ user, isLoading, refresh, logout }), [user, isLoading])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used inside AuthProvider')
  return context
}

