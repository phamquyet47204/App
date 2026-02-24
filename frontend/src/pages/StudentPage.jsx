import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../api";

export default function StudentPage({ token, user, onLogout }) {
  const [courses, setCourses] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [windowInfo, setWindowInfo] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    setError("");
    try {
      const [courseData, registrationData, windowData] = await Promise.all([
        apiRequest("/courses/", {}, token),
        apiRequest("/registrations/", {}, token),
        apiRequest("/registration-window/", {}, token),
      ]);
      setCourses(courseData);
      setRegistrations(registrationData);
      setWindowInfo(windowData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRegister = async (courseId) => {
    setMessage("");
    setError("");
    try {
      const response = await apiRequest(`/registrations/${courseId}/`, { method: "POST" }, token);
      setMessage(response.detail);
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCancel = async (courseId) => {
    setMessage("");
    setError("");
    try {
      const response = await apiRequest(`/registrations/${courseId}/`, { method: "DELETE" }, token);
      setMessage(response.detail);
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <div className="top-bar">
        <div>
          <h2>Xin chào, {user?.first_name || user?.username}</h2>
          <p>MSSV: {user?.mssv} | Email: {user?.email}</p>
        </div>
        <div className="actions">
          {user?.is_staff ? <Link to="/admin">Trang Admin</Link> : null}
          <button onClick={onLogout}>Đăng xuất</button>
        </div>
      </div>

      <div className="card">
        <h3>Trạng thái mở đăng ký</h3>
        {windowInfo ? (
          <p>
            {windowInfo.can_register ? "Đang mở" : "Đang đóng"}
            {windowInfo.start_at ? ` | Bắt đầu: ${new Date(windowInfo.start_at).toLocaleString()}` : ""}
            {windowInfo.end_at ? ` | Kết thúc: ${new Date(windowInfo.end_at).toLocaleString()}` : ""}
          </p>
        ) : (
          <p>Đang tải...</p>
        )}
      </div>

      {message ? <div className="alert success">{message}</div> : null}
      {error ? <div className="alert error">{error}</div> : null}

      <div className="grid-2">
        <div className="card">
          <h3>Danh sách môn học</h3>
          {loading ? <p>Đang tải...</p> : null}
          <table>
            <thead>
              <tr>
                <th>Mã môn</th>
                <th>Tên môn</th>
                <th>Tín chỉ</th>
                <th>Hành động</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((course) => (
                <tr key={course.id}>
                  <td>{course.code}</td>
                  <td>{course.name}</td>
                  <td>{course.credits}</td>
                  <td>
                    {course.is_registered ? (
                      <button className="danger" onClick={() => handleCancel(course.id)}>
                        Hủy đăng ký
                      </button>
                    ) : (
                      <button onClick={() => handleRegister(course.id)}>Đăng ký</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h3>Môn đã đăng ký</h3>
          {registrations.length === 0 ? <p>Chưa có môn học nào.</p> : null}
          <ul>
            {registrations.map((registration) => (
              <li key={registration.id}>
                {registration.course.code} - {registration.course.name}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
