import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Checkbox, List, Typography, Image, Space } from "antd";
import api from "../api";

const { Paragraph } = Typography;

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [selectedProjects, setSelectedProjects] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.get("/projects/");
        setProjects(response.data);
      } catch (err) {
        console.error("Ошибка при получении проектов:", err);
        setError("Не удалось загрузить проекты");
      }
    };

    fetchProjects();
  }, []);

  const handleCheckboxChange = (projectId) => {
    setSelectedProjects((prevSelected) =>
      prevSelected.includes(projectId)
        ? prevSelected.filter((id) => id !== projectId)
        : [...prevSelected, projectId]
    );
  };

  const deleteProjectByID = async (projectID) => {
    try {
      await api.delete(`/projects/${projectID}`);
    } catch (err) {
      console.error("Ошибка при удалении:", err);
      if (err.response?.status === 404) {
        setError("Проект не найден");
      } else if (err.response?.data?.detail) {
        setError(`Ошибка: ${err.response.data.detail}`);
      } else {
        setError("Неизвестная ошибка при удалении");
      }
    }
  };

  const handleDeletion = async () => {
    if (selectedProjects.length !== 0) {
      const confirmed = window.confirm(
        "Вы уверены, что хотите удалить выбранные проекты?"
      );
      if (!confirmed) return;
    }

    for (const id of selectedProjects) {
      await deleteProjectByID(id);
    }

    setProjects(
      projects.filter((project) => !selectedProjects.includes(project.id))
    );
    setSelectedProjects([]);
  };

  const handleCreation = () => {
    navigate("/projects/create");
  };

  return (
    <div>
      <h2>Список проектов</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div style={{ marginBottom: "1em" }}>
        <Button
          onClick={handleCreation}
          type="primary"
          style={{ marginRight: "10px" }}
        >
          Создать
        </Button>
        <Button onClick={handleDeletion} type="danger">
          Удалить
        </Button>
      </div>
      <div style={{ maxHeight: "400px", overflowY: "auto" }}>
        {projects.length === 0 ? (
          <p>Нет проектов для отображения.</p>
        ) : (
          <List
            dataSource={projects}
            renderItem={(project) => (
              <List.Item key={project.id} style={{ marginBottom: "1em" }}>
                <Space direction="vertical" style={{ width: "100%" }}>
                  <Checkbox
                    checked={selectedProjects.includes(project.id)}
                    onChange={() => handleCheckboxChange(project.id)}
                  >
                    {project.title}
                  </Checkbox>
                  <Paragraph ellipsis={{ rows: 2, expandable: true }}>
                    {project.description}
                  </Paragraph>
                  {project.image_url && (
                    <Image
                      src={project.image_url}
                      alt={project.title}
                      style={{
                        maxWidth: "200px",
                        display: "block",
                        marginTop: "0.5em",
                      }}
                    />
                  )}
                  <Button
                    onClick={() => navigate(`/projects/${project.id}`)}
                    type="link"
                    style={{ marginTop: "0.5em" }}
                  >
                    Редактировать
                  </Button>
                </Space>
              </List.Item>
            )}
          />
        )}
      </div>
    </div>
  );
}
