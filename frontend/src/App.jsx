import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiRequest } from "./api";
import LoginPage from "./pages/LoginPage";
import StudentPage from "./pages/StudentPage";
import AdminPage from "./pages/AdminPage";

function PrivateRoute({ token, children }) {
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default function App() {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(() => {
    const data = localStorage.getItem("user");
    return data ? JSON.parse(data) : null;
  });

  useEffect(() => {
    if (!token) {
      return;
    }

    apiRequest("/auth/me/", {}, token)
      .then((me) => {
        setUser(me);
        localStorage.setItem("user", JSON.stringify(me));
      })
      .catch(() => {
        handleLogout();
      });
  }, [token]);

  const handleLogin = (payload) => {
    setToken(payload.token);
    setUser(payload.user);
    localStorage.setItem("token", payload.token);
    localStorage.setItem("user", JSON.stringify(payload.user));

    if (payload.user.is_staff) {
      navigate("/admin", { replace: true });
    } else {
      navigate("/", { replace: true });
    }
  };

  const handleLogout = async () => {
    const currentToken = localStorage.getItem("token");
    if (currentToken) {
      try {
        await apiRequest("/auth/logout/", { method: "POST" }, currentToken);
      } catch {
        // ignore
      }
    }

    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
    navigate("/login", { replace: true });
  };

  return (
    <Routes>
      <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
      <Route
        path="/"
        element={
          <PrivateRoute token={token}>
            <StudentPage token={token} user={user} onLogout={handleLogout} />
          </PrivateRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <PrivateRoute token={token}>
            <AdminPage token={token} user={user} onLogout={handleLogout} />
          </PrivateRoute>
        }
      />
      <Route path="*" element={<Navigate to={token ? "/" : "/login"} replace />} />
    </Routes>
  );
}
