import { useEffect, useState } from "react";
import {
  Alert,
  Badge,
  Card,
  Container,
  Divider,
  Group,
  Loader,
  Stack,
  Text,
  Title,
} from "@mantine/core";

import { getMe } from "../api";

type User = {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  role: string;
};

type Props = {
  token: string;
};

export default function ProfilePage({ token }: Props) {
  const [user, setUser] = useState<User | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadUser() {
      try {
        const result = await getMe(token);
        setUser(result);
      } catch (error) {
        setMessage(
          error instanceof Error
            ? error.message
            : "Could not load user"
        );
      }
    }

    if (token) {
      loadUser();
    }
  }, [token]);

  if (!token) {
    return (
      <Container size="sm" py="xl">
        <Alert color="yellow">
          Please login first.
        </Alert>
      </Container>
    );
  }

  if (message) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red" title="Could not load profile">
          {message}
        </Alert>
      </Container>
    );
  }

  if (!user) {
    return (
      <Container size="sm" py="xl">
        <Group justify="center">
          <Loader />
        </Group>
      </Container>
    );
  }

  return (
    <Container size="sm" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={1}>Profile</Title>

          <Text c="dimmed" mt={4}>
            Your account information
          </Text>
        </div>

        <Card
          withBorder
          shadow="sm"
          padding="xl"
          radius="md"
        >
          <Stack gap="md">
            <Group justify="space-between">
              <Text fw={600}>Account status</Text>

              <Badge
                color={user.is_active ? "green" : "red"}
              >
                {user.is_active ? "Active" : "Inactive"}
              </Badge>
            </Group>

            <Divider />

            <div>
              <Text size="sm" c="dimmed">
                Username
              </Text>

              <Text fw={500}>
                {user.username}
              </Text>
            </div>

            <div>
              <Text size="sm" c="dimmed">
                Email
              </Text>

              <Text fw={500}>
                {user.email}
              </Text>
            </div>

            <div>
              <Text size="sm" c="dimmed">
                Role
              </Text>

              <Badge variant="light">
                {user.role}
              </Badge>
            </div>

            <div>
              <Text size="sm" c="dimmed">
                User ID
              </Text>

              <Text size="sm" ff="monospace">
                {user.id}
              </Text>
            </div>
          </Stack>
        </Card>
      </Stack>
    </Container>
  );
}
