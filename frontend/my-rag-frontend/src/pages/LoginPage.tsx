import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Alert,
  Anchor,
  Button,
  Container,
  Paper,
  PasswordInput,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";

import { loginUser } from "../api";

type Props = {
  onLogin: (token: string) => void;
};

export default function LoginPage({ onLogin }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  async function handleLogin() {
    setMessage("");

    try {
      const result = await loginUser(email, password);

      onLogin(result.access_token);
      navigate("/me");
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Login failed"
      );
    }
  }

  return (
    <Container size={420} my={80}>
      <Title ta="center" mb="xs">
        Welcome back
      </Title>

      <Text c="dimmed" size="sm" ta="center" mb="xl">
        Sign in to your RAG Banking account
      </Text>

      <Paper withBorder shadow="md" p="xl" radius="md">
        <Stack>
          <TextInput
            label="Email"
            placeholder="you@example.com"
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(event.currentTarget.value)
            }
            required
          />

          <PasswordInput
            label="Password"
            placeholder="Your password"
            value={password}
            onChange={(event) =>
              setPassword(event.currentTarget.value)
            }
            required
          />

          {message && (
            <Alert color="red" title="Login failed">
              {message}
            </Alert>
          )}

          <Button
            fullWidth
            size="md"
            onClick={handleLogin}
          >
            Login
          </Button>

          <Text size="sm" ta="center">
            Don't have an account?{" "}
            <Anchor component={Link} to="/register">
              Register
            </Anchor>
          </Text>
        </Stack>
      </Paper>
    </Container>
  );
}

