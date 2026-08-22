import { useState } from "react";
import { Link } from "react-router-dom";
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

import { registerUser } from "../api";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleRegister() {
    setMessage("");

    try {
      const user = await registerUser(
        username,
        email,
        password
      );

      setMessage(`Registered ${user.username}`);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Registration failed"
      );
    }
  }

  return (
    <Container size={420} my={80}>
      <Title ta="center" mb="xs">
        Create an account
      </Title>

      <Text c="dimmed" size="sm" ta="center" mb="xl">
        Create your RAG Banking account
      </Text>

      <Paper withBorder shadow="md" p="xl" radius="md">
        <Stack>
          <TextInput
            label="Username"
            placeholder="Your username"
            value={username}
            onChange={(event) =>
              setUsername(event.currentTarget.value)
            }
            required
          />

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
            placeholder="Create a password"
            value={password}
            onChange={(event) =>
              setPassword(event.currentTarget.value)
            }
            required
          />

          {message && (
            <Alert color="green">
              {message}
            </Alert>
          )}

          <Button
            fullWidth
            size="md"
            onClick={handleRegister}
          >
            Register
          </Button>

          <Text size="sm" ta="center">
            Already have an account?{" "}
            <Anchor component={Link} to="/login">
              Login
            </Anchor>
          </Text>
        </Stack>
      </Paper>
    </Container>
  );
}
