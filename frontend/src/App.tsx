import { useState, useEffect } from 'react'
import './App.css'

interface Post {
  id: number
  caption: string
  image?: string
  video?: string
  created_at: string
  user: {
    username: string
    profile_picture?: string
  }
  likes_count?: number
  comments_count?: number
}

interface Story {
  id: number
  image?: string
  video?: string
  created_at: string
  user: {
    username: string
    profile_picture?: string
  }
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [posts, setPosts] = useState<Post[]>([])
  const [stories, setStories] = useState<Story[]>([])
  const [feedLoading, setFeedLoading] = useState(false)
  const [likedPosts, setLikedPosts] = useState<Set<number>>(new Set())

  useEffect(() => {
    const token = localStorage.getItem('access')
    if (token) {
      setIsAuthenticated(true)
      fetchFeed()
    }
  }, [])

  const fetchFeed = async () => {
    setFeedLoading(true)
    try {
      const token = localStorage.getItem('access')
      
      const [postsRes, storiesRes] = await Promise.all([
        fetch('http://127.0.0.1:8000/api/posts/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }),
        fetch('http://127.0.0.1:8000/api/stories/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }),
      ])

      if (postsRes.ok) {
        const postsData = await postsRes.json()
        setPosts(postsData.results || postsData)
      }

      if (storiesRes.ok) {
        const storiesData = await storiesRes.json()
        setStories(storiesData.results || storiesData)
      }
    } catch (err) {
      console.error('Error fetching feed:', err)
    } finally {
      setFeedLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const endpoint = isLogin ? 'login' : 'register'
      const response = await fetch(`http://127.0.0.1:8000/api/${endpoint}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Ошибка')
      }

      if (isLogin) {
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        setIsAuthenticated(true)
        fetchFeed()
      } else {
        alert('Регистрация успешна!')
        setIsLogin(true)
      }
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleLogout = () => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    setIsAuthenticated(false)
    setPosts([])
    setStories([])
  }

  const handleLike = (postId: number) => {
    setLikedPosts(prev => {
      const newLiked = new Set(prev)
      if (newLiked.has(postId)) {
        newLiked.delete(postId)
      } else {
        newLiked.add(postId)
      }
      return newLiked
    })
  }

  if (!isAuthenticated) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="auth-box">
            <div className="instagram-logo">Instagram</div>
            
            {error && <div className="error-message">{error}</div>}
            
            <form onSubmit={handleSubmit} className="auth-form">
              {!isLogin && (
                <input
                  type="email"
                  name="email"
                  placeholder="Мобильный номер или эл. адрес"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              )}
              
              <input
                type="text"
                name="username"
                placeholder="Имя пользователя"
                value={formData.username}
                onChange={handleChange}
                required
              />
              
              <input
                type="password"
                name="password"
                placeholder="Пароль"
                value={formData.password}
                onChange={handleChange}
                required
              />
              
              <button type="submit" disabled={loading} className="auth-button">
                {loading ? 'Загрузка...' : isLogin ? 'Войти' : 'Зарегистрироваться'}
              </button>
            </form>
            
            <div className="auth-divider">
              <div className="line"></div>
              <span>ИЛИ</span>
              <div className="line"></div>
            </div>
            
            <button className="facebook-login">
              <span>Войти через Facebook</span>
            </button>
            
            {isLogin && (
              <a href="#" className="forgot-password">Забыли пароль?</a>
            )}
          </div>
          
          <div className="auth-switch">
            {isLogin ? (
              <>
                <span>У вас нет аккаунта?</span>
                <button onClick={() => setIsLogin(false)} className="switch-link">
                  Зарегистрироваться
                </button>
              </>
            ) : (
              <>
                <span>Уже есть аккаунт?</span>
                <button onClick={() => setIsLogin(true)} className="switch-link">
                  Войти
                </button>
              </>
            )}
          </div>
          
          <div className="app-download">
            <p>Установите приложение.</p>
            <div className="app-buttons">
              <button className="app-button">App Store</button>
              <button className="app-button">Google Play</button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="instagram-app">
      <nav className="navbar">
        <div className="navbar-content">
          <div className="navbar-logo">Instagram</div>
          
          <div className="navbar-search">
            <span className="search-icon">🔍</span>
            <input type="text" placeholder="Поиск" />
          </div>
          
          <div className="navbar-icons">
            <button className="nav-icon" title="Главная">🏠</button>
            <button className="nav-icon" title="Сообщения">💬</button>
            <button className="nav-icon" title="Создать">➕</button>
            <button className="nav-icon" title="Эксплорер">🧭</button>
            <button className="nav-icon" title="Уведомления">❤️</button>
            <button className="nav-icon profile-icon" title="Профиль">👤</button>
            <button onClick={handleLogout} className="nav-icon" title="Выйти">🚪</button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <div className="feed-container">
          <div className="stories-bar">
            {feedLoading ? (
              <div className="loading">Загрузка...</div>
            ) : stories.length === 0 ? (
              <div className="no-stories">Нет историй</div>
            ) : (
              stories.map((story) => (
                <div key={story.id} className="story-circle">
                  <div className="story-ring">
                    {story.user.profile_picture ? (
                      <img src={story.user.profile_picture} alt={story.user.username} />
                    ) : (
                      <div className="story-avatar-placeholder">{story.user.username[0].toUpperCase()}</div>
                    )}
                  </div>
                  <span>{story.user.username}</span>
                </div>
              ))
            )}
          </div>

          <div className="posts-feed">
            {feedLoading ? (
              <div className="loading">Загрузка...</div>
            ) : posts.length === 0 ? (
              <div className="no-posts">Нет постов</div>
            ) : (
              posts.map((post) => (
                <article key={post.id} className="post-card">
                  <div className="post-header">
                    <div className="post-user">
                      {post.user.profile_picture ? (
                        <img src={post.user.profile_picture} alt={post.user.username} />
                      ) : (
                        <div className="user-avatar">{post.user.username[0].toUpperCase()}</div>
                      )}
                      <span className="username">{post.user.username}</span>
                    </div>
                    <button className="more-options">•••</button>
                  </div>

                  {post.image && (
                    <img src={post.image} alt="Post" className="post-media" />
                  )}
                  
                  {post.video && (
                    <video src={post.video} controls className="post-media" />
                  )}

                  <div className="post-actions">
                    <div className="action-buttons">
                      <button 
                        className={`action-btn ${likedPosts.has(post.id) ? 'liked' : ''}`}
                        onClick={() => handleLike(post.id)}
                        title="Нравится"
                      >
                        {likedPosts.has(post.id) ? '❤️' : '🤍'}
                      </button>
                      <button className="action-btn" title="Комментировать">💬</button>
                      <button className="action-btn" title="Поделиться">✈️</button>
                      <button className="action-btn save-btn" title="Сохранить">🔖</button>
                    </div>
                  </div>

                  <div className="post-info">
                    <span className="likes-count">{post.likes_count || 0} отметок "Нравится"</span>
                    <div className="post-caption">
                      <span className="caption-username">{post.user.username}</span>
                      <span className="caption-text">{post.caption}</span>
                    </div>
                    {post.comments_count > 0 && (
                      <button className="view-comments">Посмотреть все комментарии ({post.comments_count})</button>
                    )}
                    <span className="post-time">{new Date(post.created_at).toLocaleDateString('ru-RU')}</span>
                  </div>

                  <div className="add-comment">
                    <span className="emoji-btn">😊</span>
                    <input type="text" placeholder="Добавить комментарий..." />
                    <button className="post-comment-btn">Опубликовать</button>
                  </div>
                </article>
              ))
            )}
          </div>
        </div>

        <aside className="sidebar">
          <div className="sidebar-user">
            <div className="user-avatar-large">👤</div>
            <div className="user-info">
              <span className="sidebar-username">username</span>
              <span className="sidebar-fullname">Полное имя</span>
            </div>
            <button className="switch-account">Переключиться</button>
          </div>

          <div className="sidebar-suggestions">
            <div className="suggestions-header">
              <span>Рекомендации для вас</span>
              <button className="see-all">Все</button>
            </div>
            
            <div className="suggestion-item">
              <div className="suggestion-avatar">👤</div>
              <div className="suggestion-info">
                <span className="suggestion-username">user1</span>
                <span className="suggestion-reason">Новое для вас</span>
              </div>
              <button className="follow-btn">Подписаться</button>
            </div>
            
            <div className="suggestion-item">
              <div className="suggestion-avatar">👤</div>
              <div className="suggestion-info">
                <span className="suggestion-username">user2</span>
                <span className="suggestion-reason">Рекомендуется</span>
              </div>
              <button className="follow-btn">Подписаться</button>
            </div>
          </div>

          <div className="sidebar-footer">
            <a href="#" className="footer-link">О нас</a> •
            <a href="#" className="footer-link">Помощь</a> •
            <a href="#" className="footer-link">Пресса</a> •
            <a href="#" className="footer-link">API</a> •
            <a href="#" className="footer-link">Вакансии</a> •
            <a href="#" className="footer-link">Конфиденциальность</a> •
            <a href="#" className="footer-link">Условия</a>
            <p className="copyright">© 2024 INSTAGRAM FROM META</p>
          </div>
        </aside>
      </main>
    </div>
  )
}

export default App