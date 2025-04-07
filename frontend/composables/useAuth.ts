export const useAuth = () => {
    const user = useState('user', () => null)
  
    function login(username: string, password: string) {
      // TODO: später echte API-Authentifizierung hier
      if (username === 'admin' && password === 'pass') {
        user.value = { name: 'admin' }
        return true
      }
      return false
    }
  
    function logout() {
      user.value = null
      navigateTo('/login')
    }
  
    return { user, login, logout }
  }
  