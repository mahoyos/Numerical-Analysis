# Test Documentation

## Objective
This test suite validates critical numerical logic, API response contracts, frontend integration contracts, and UI helper behaviors. The test architecture mirrors each project structure under dedicated test roots:

- Backend tests: `backend/tests/...`
- Frontend tests: `frontend/tests/src/...`

Coverage target configured in both projects is minimum 90% for the selected unit-test scope.

## Backend Scenarios

### Models
- `backend/tests/models/test_non_linear_equations.py`
- `backend/tests/models/test_system_equations.py`
- `backend/tests/models/test_interpolation.py`

What is validated:
- Valid payload parsing for Pydantic models.
- Validation errors when enum-like `Literal` fields receive invalid values.

Why:
- Input validation is the first defense for numerical algorithms and API correctness.

### Utilities
- `backend/tests/utils/test_math_operations.py`
- `backend/tests/utils/test_error_type.py`
- `backend/tests/utils/test_system_equations.py`
- `backend/tests/utils/errors/test_errors.py`

What is validated:
- Symbolic math evaluation and derivative generation.
- Absolute/relative error formulas (scalar and vector).
- Residual convergence verification and spectral radius calculations.
- Error classes and error code integrity.

Why:
- These utilities are foundational to all methods; a bug here propagates globally.

### Response and Exception Handlers
- `backend/tests/utils/handlers/test_response.py`
- `backend/tests/utils/handlers/test_non_linear_equations_handler.py`
- `backend/tests/utils/handlers/test_system_equations_handler.py`

What is validated:
- Uniform success/error response shape.
- Mapping of known/unknown exceptions into domain error codes.

Why:
- The frontend depends on stable response contracts for user feedback and rendering.

### Services
- `backend/tests/services/test_non_linear_equations_service.py`
- `backend/tests/services/test_system_equations_service.py`
- `backend/tests/services/test_interpolation_service.py`

What is validated:
- Successful execution paths for core methods.
- Representative error branches (e.g., invalid interval in false position, unstable matrix in SOR).

Why:
- Services implement core numerical behavior and business rules.

### Routers
- `backend/tests/routers/test_non_linear_equations_router.py`
- `backend/tests/routers/test_system_equations_router.py`
- `backend/tests/routers/test_interpolation_router.py`

What is validated:
- End-to-end request/response shape through FastAPI routes.
- HTTP status and payload structure for representative scenarios.

Why:
- Verifies integration between model validation, service execution, and serialization.

## Frontend Scenarios

### Services
- `frontend/tests/src/services/NonLinearEquationsService.test.ts`
- `frontend/tests/src/services/SystemsEquationsService.test.ts`
- `frontend/tests/src/services/InterpolationsService.test.ts`

What is validated:
- Axios request execution and success payload forwarding.
- Error propagation for failed HTTP requests.

Why:
- Service layer reliability is required for deterministic behavior in all views.

### Utilities
- `frontend/tests/src/util/ChartUtils.test.ts`
- `frontend/tests/src/util/DownloadChartUtils.test.ts`

What is validated:
- Expression sanitization rules.
- Canvas-to-SVG export flow (blob creation, anchor click, URL revocation).
- Defensive behavior when canvas is absent.

Why:
- Utility bugs can silently break chart rendering and export actions.

### Router
- `frontend/tests/src/router/index.test.ts`

What is validated:
- Registration of primary and detail routes.

Why:
- Broken route registration blocks user navigation to numerical methods.

### Components
- `frontend/tests/src/components/BreadCrumb.test.ts`
- `frontend/tests/src/components/AppModal.test.ts`
- `frontend/tests/src/components/SystemsEquationsDataTable.test.ts`

What is validated:
- Breadcrumb rendering for link and plain items.
- Modal exposed methods (`launch`, `modifyMessage`, `close`) and state transitions.
- Data table pagination behavior.

Why:
- These reusable components affect many user flows and feedback patterns.

## How to Run

### Backend
1. Install dependencies:
   - `pip install -r backend/requirements.txt -r backend/requirements-dev.txt`
2. Run tests with coverage:
   - `cd backend`
   - `pytest`

### Frontend
1. Install dependencies:
   - `cd frontend`
   - `npm install`
2. Run unit tests:
   - `npm run test:unit:vitest`
3. Run coverage:
   - `npm run test:coverage`

## Notes
- Backend `requirements.txt` is encoded in UTF-16 LE in this repository; keep that in mind for tooling.
- Coverage thresholds are enforced by configuration:
  - Backend: `backend/pytest.ini`
  - Frontend: `frontend/vite.config.ts`
