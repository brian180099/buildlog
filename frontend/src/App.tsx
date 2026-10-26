import { NavLink, Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import './App.css'
import { AuthProvider, useAuth } from './auth/AuthContext'
import { RequireAuth } from './components/RequireAuth'
import { AccountPage } from './pages/AccountPage'
import { FoundationPage } from './pages/FoundationPage'
import { LoginPage } from './pages/LoginPage'
import { PlaceholderPage } from './pages/PlaceholderPage'
import { RegisterPage } from './pages/RegisterPage'

const navigation = [
  { to: '/', label: '개발 상태', end: true },
  { to: '/study', label: '공부 기록' },
  { to: '/todos', label: '할 일' },
  { to: '/errors', label: '오류 기록' },
  { to: '/public', label: '공개 기록' },
]

function AppContent() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <NavLink className="brand" to="/">
          <span className="brand-mark">B</span>
          <span>
            <strong>BuildLog</strong>
            <small>배운 것을 쌓는 개발 기록</small>
          </span>
        </NavLink>
        {user && (
          <div className="header-actions">
            <nav aria-label="주요 메뉴">
              {navigation.map((item) => (
                <NavLink
                  className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
                  end={item.end}
                  key={item.to}
                  to={item.to}
                >
                  {item.label}
                </NavLink>
              ))}
              <NavLink className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} to="/account">
                계정
              </NavLink>
            </nav>
            <button className="logout-button" onClick={handleLogout} type="button">
              로그아웃
            </button>
          </div>
        )}
      </header>

      <main>
        <Routes>
          <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
          <Route path="/register" element={user ? <Navigate to="/" replace /> : <RegisterPage />} />
          <Route path="/" element={<RequireAuth><FoundationPage /></RequireAuth>} />
          <Route path="/account" element={<RequireAuth><AccountPage /></RequireAuth>} />
          <Route path="/study" element={<RequireAuth><PlaceholderPage title="공부 기록" phase="Phase 4" /></RequireAuth>} />
          <Route path="/todos" element={<RequireAuth><PlaceholderPage title="할 일" phase="Phase 5" /></RequireAuth>} />
          <Route path="/errors" element={<RequireAuth><PlaceholderPage title="오류 기록" phase="Phase 6" /></RequireAuth>} />
          <Route path="/public" element={<RequireAuth><PlaceholderPage title="공개 기록" phase="Phase 7" /></RequireAuth>} />
          <Route path="*" element={<PlaceholderPage title="페이지를 찾을 수 없습니다" />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

