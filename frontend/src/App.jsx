import { BrowserRouter, Routes, Route } from "react-router-dom";
import RegisterPage from "./components/RegisterPage";
import LoginPage from "./components/LoginPage";
import ProjectsPage from "./components/ProjectsPage";
import CreateEditProjectPage from "./components/CreateEditProjectPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/create" element={<CreateEditProjectPage />} />
        <Route
          path="/projects/:projectId"
          element={<CreateEditProjectPage />}
        />
        {}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
