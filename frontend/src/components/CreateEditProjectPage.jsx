import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Form, Input, Button, Typography, Image, Upload, message } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import api from "../api";

const { Title } = Typography;
const { TextArea } = Input;

export default function CreateEditProjectPage() {
  const { projectId } = useParams();
  const [form] = Form.useForm();
  const [imageFile, setImageFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const isEditMode = Boolean(projectId);

  useEffect(() => {
    if (isEditMode) {
      const fetchProject = async () => {
        setLoading(true);
        try {
          const response = await api.get(`/projects/${projectId}`);
          const { title, description, image_url } = response.data;
          form.setFieldsValue({ title, description });
          setImageUrl(image_url);
        } catch (err) {
          setError("Не удалось загрузить проект");
        } finally {
          setLoading(false);
        }
      };
      fetchProject();
    }
  }, [projectId, form, isEditMode]);

  const handleSubmit = async (values) => {
    const formData = new FormData();
    formData.append("title", values.title);
    formData.append("description", values.description);
    if (imageFile) {
      formData.append("image_file", imageFile);
    }

    try {
      if (isEditMode) {
        await api.put(`/projects/${projectId}`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      } else {
        await api.post("/projects/create", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      }
      navigate("/projects");
    } catch (err) {
      console.error("Ошибка при сохранении проекта:", err);
      setError("Не удалось сохранить проект");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 24 }}>
      <Title level={2}>
        {isEditMode ? "Редактирование проекта" : "Создание проекта"}
      </Title>

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          title: "",
          description: "",
        }}
      >
        <Form.Item
          label="Название"
          name="title"
          rules={[{ required: true, message: "Введите название проекта" }]}
        >
          <Input placeholder="Название проекта" />
        </Form.Item>

        <Form.Item
          label="Описание"
          name="description"
          rules={[{ required: false, message: "Введите описание проекта" }]}
        >
          <TextArea placeholder="Описание проекта" rows={4} />
        </Form.Item>

        {imageUrl && (
          <div style={{ marginBottom: 16 }}>
            <p>Текущее изображение:</p>
            <Image
              src={imageUrl}
              alt="project"
              style={{
                maxWidth: "200px",
                display: "block",
                marginTop: "0.5em",
              }}
            />
          </div>
        )}

        <Form.Item label="Изображение">
          <Upload
            beforeUpload={(file) => {
              setImageFile(file);
              return false;
            }}
            maxCount={1}
            accept="image/*"
          >
            <Button icon={<UploadOutlined />}>Выбрать изображение</Button>
          </Upload>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            {isEditMode ? "Сохранить изменения" : "Создать"}
          </Button>
        </Form.Item>
      </Form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
