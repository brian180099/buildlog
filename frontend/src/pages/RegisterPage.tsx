import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { submitAuthRequest, useAuth } from '../auth/AuthContext'

export function RegisterPage() {
  const navigate = useNavigate()
  const { refresh } = useAuth()
  const [form, setForm] = useState({ email: '', password: '', nickname: '' })
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      await submitAuthRequest('register', form)
      await refresh()
      navigate('/', { replace: true })
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : '회원가입에 실패했습니다.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="auth-layout">
      <div className="auth-card">
        <p className="eyebrow">BuildLog 시작하기</p>
        <h1>회원가입</h1>
        <p className="auth-description">공부 기록을 쌓을 계정을 만들어보세요.</p>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            이메일
            <input
              autoComplete="email"
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              required
              type="email"
              value={form.email}
            />
          </label>
          <label>
            비밀번호
            <input
              autoComplete="new-password"
              minLength={8}
              maxLength={64}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              required
              type="password"
              value={form.password}
            />
          </label>
          <label>
            닉네임
            <input
              autoComplete="nickname"
              minLength={2}
              maxLength={20}
              onChange={(event) => setForm({ ...form, nickname: event.target.value })}
              required
              value={form.nickname}
            />
          </label>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button disabled={isSubmitting} type="submit">
            {isSubmitting ? '가입 중...' : '회원가입'}
          </button>
        </form>
        <p className="auth-footer">
          이미 계정이 있나요? <Link to="/login">로그인</Link>
        </p>
      </div>
    </section>
  )
}

