import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { apiRequest } from "../api";

export default function AdminPage({ token, user, onLogout }) {
  const [form, setForm] = useState({
    is_open: false,
    start_at: "",
    end_at: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadWindow = async () => {
    setError("");
    try {
      const data = await apiRequest("/admin/registration-window/", {}, token);
      setForm({
        is_open: data.is_open,
        start_at: data.start_at ? data.start_at.slice(0, 16) : "",
        end_at: data.end_at ? data.end_at.slice(0, 16) : "",
      });
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadWindow();
  }, []);

  if (!user?.is_staff) {
    return <Navigate to="/" replace />;
  }

  const saveWindow = async (payload) => {
    setMessage("");
    setError("");

    try {
      await apiRequest(
        "/admin/registration-window/",
        {
          method: "PUT",
          body: JSON.stringify(payload),
        },
        token
      );
      setMessage("Cập nhật trạng thái đăng ký thành công.");
      await loadWindow();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await saveWindow({
      is_open: form.is_open,
      start_at: form.start_at ? new Date(form.start_at).toISOString() : null,
      end_at: form.end_at ? new Date(form.end_at).toISOString() : null,
    });
  };

  const handleCloseNow = async () => {
    setForm({ is_open: false, start_at: "", end_at: "" });
    await saveWindow({ is_open: false, start_at: null, end_at: null });
  };

  const handleOpenNow = async () => {
    setForm({ is_open: true, start_at: "", end_at: "" });
    await saveWindow({ is_open: true, start_at: null, end_at: null });
  };

  return (
    <div className="container">
      <div className="top-bar">
        <div>
          <h2>Trang Admin</h2>
          <p>Điều chỉnh thời gian mở/đóng đăng ký môn học</p>
        </div>
        <div className="actions">
          <Link to="/">Trang sinh viên</Link>
          <button onClick={onLogout}>Đăng xuất</button>
        </div>
      </div>

      <form className="card" onSubmit={handleSubmit}>
        <label>
          <input
            type="checkbox"
            checked={form.is_open}
            onChange={(e) => setForm((prev) => ({ ...prev, is_open: e.target.checked }))}
          />
          Mở hệ thống đăng ký môn học
        </label>

        <label>Thời gian bắt đầu</label>
        <input
          type="datetime-local"
          value={form.start_at}
          onChange={(e) => setForm((prev) => ({ ...prev, start_at: e.target.value }))}
        />

        <label>Thời gian kết thúc</label>
        <input
          type="datetime-local"
          value={form.end_at}
          onChange={(e) => setForm((prev) => ({ ...prev, end_at: e.target.value }))}
        />

        {message ? <div className="alert success">{message}</div> : null}
        {error ? <div className="alert error">{error}</div> : null}

        <div className="actions">
          <button type="submit">Lưu cấu hình</button>
          <button type="button" onClick={handleOpenNow}>
            Mở đăng ký ngay
          </button>
          <button type="button" className="danger" onClick={handleCloseNow}>
            Đóng đăng ký ngay
          </button>
        </div>
      </form>
    </div>
  );
}
