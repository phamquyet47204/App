import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL;

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '90s', target: 120 },
    { duration: '60s', target: 120 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.2'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/`);
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
