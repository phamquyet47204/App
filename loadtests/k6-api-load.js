import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const IDENTIFIER = __ENV.IDENTIFIER || 'sv001';
const PASSWORD = __ENV.PASSWORD || 'python123';
const THINK_TIME = Number(__ENV.THINK_TIME || 0.3);

const VUS = Number(__ENV.VUS || 30);
const DURATION = __ENV.DURATION || '2m';

export const options = {
  stages: [
    { duration: '30s', target: Math.max(1, Math.floor(VUS * 0.3)) },
    { duration: '45s', target: Math.max(1, Math.floor(VUS * 0.6)) },
    { duration: DURATION, target: VUS },
    { duration: '20s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1200'],
    checks: ['rate>0.95'],
  },
};

function jsonHeaders(token) {
  return {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`,
    },
  };
}

export default function () {
  const loginRes = http.post(
    `${BASE_URL}/api/auth/login/`,
    JSON.stringify({ identifier: IDENTIFIER, password: PASSWORD }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  const loginOk = check(loginRes, {
    'login status 200': (r) => r.status === 200,
    'login returns token': (r) => {
      try {
        return !!r.json('token');
      } catch (e) {
        return false;
      }
    },
  });

  if (!loginOk) {
    sleep(THINK_TIME);
    return;
  }

  const token = loginRes.json('token');
  const auth = jsonHeaders(token);

  const meRes = http.get(`${BASE_URL}/api/auth/me/`, auth);
  check(meRes, {
    'me status 200': (r) => r.status === 200,
  });

  const coursesRes = http.get(`${BASE_URL}/api/courses/`, auth);
  const coursesOk = check(coursesRes, {
    'courses status 200': (r) => r.status === 200,
    'courses is array': (r) => {
      try {
        return Array.isArray(r.json());
      } catch (e) {
        return false;
      }
    },
  });

  const regsRes = http.get(`${BASE_URL}/api/registrations/`, auth);
  check(regsRes, {
    'registrations status 200': (r) => r.status === 200,
  });

  const healthRes = http.get(`${BASE_URL}/api/healthz/`);
  check(healthRes, {
    'healthz status 200': (r) => r.status === 200,
  });

  if (coursesOk) {
    const list = coursesRes.json();
    if (Array.isArray(list) && list.length > 0) {
      const index = Math.floor(Math.random() * list.length);
      const courseId = list[index]?.id;
      if (courseId) {
        const registerRes = http.post(`${BASE_URL}/api/registrations/${courseId}/`, null, auth);
        check(registerRes, {
          'register expected status': (r) => [201, 400].includes(r.status),
        });
      }
    }
  }

  sleep(THINK_TIME);
}
