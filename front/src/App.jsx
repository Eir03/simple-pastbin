import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PastPage from './components/PastPage'
import Header from './components/Header';
import Body from './components/Body';
import './index.css'
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <Header/>
      <Routes>
        {/* Главная страница */}
        <Route path="/" element={<Body />} />
        {/* Настройка маршрута с параметром :id */}
        <Route path="/:id" element={<PastPage />} />
      </Routes>
      <Footer/>
    </Router>
  );
}

export default App;