import { useState } from 'react'
import type { FormEvent } from 'react'
import { updateNickname, useAuth } from '../auth/AuthContext'

export function AccountPage() {
  const { user, refresh } = useAuth()
  const [nickname, setNickname] = useState(user?.nickname ?? '')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      await updateNickname(nickname)
      await refresh()
      setMessage('닉네임을 변경했습니다.')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : '닉네임 변경에 실패했습니다.')
    }
  }

  return (
    <section className="page-heading">
      <p className="eyebrow">Account</p>
      <h1>계정 설정</h1>
      <p className="account-summary">
        <strong>{user?.nickname}</strong>님으로 로그인했습니다.
        <br />
        {user?.email}
      </p>
      <form className="auth-form account-form" onSubmit={handleSubmit}>
        <label>
          새 닉네임
          <input
            maxLength={20}
            minLength={2}
            onChange={(event) => setNickname(event.target.value)}
            required
            value={nickname}
          />
        </label>
        {error && <p className="form-error" role="alert">{error}</p>}
        {message && <p className="form-success" role="status">{message}</p>}
        <button type="submit">닉네임 변경</button>
      </form>
    </section>
  )
}

