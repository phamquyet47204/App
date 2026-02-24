import { useState } from "react";
import { apiRequest } from "../api";

export default function LoginPage({ onLogin }) {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await apiRequest("/auth/login/", {
        method: "POST",
        body: JSON.stringify({ identifier, password }),
      });
      onLogin(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container center-box">
      <form className="card" onSubmit={handleSubmit}>
        <h1>Đăng nhập</h1>
        <p>Dùng MSSV hoặc email và mật khẩu</p>

        <label>MSSV / Email</label>
        <input
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          placeholder="VD: 20123456 hoặc sv@domain.com"
          required
        />

        <label>Mật khẩu</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Nhập mật khẩu"
          required
        />

        {error ? <div className="alert error">{error}</div> : null}

        <button disabled={loading} type="submit">
          {loading ? "Đang xử lý..." : "Đăng nhập"}
        </button>
      </form>
    </div>
  );
}
