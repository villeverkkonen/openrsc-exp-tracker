require("@testing-library/jest-dom");
require("@testing-library/svelte");
import { render, screen, waitFor } from "@testing-library/svelte";
import { rest } from "msw";
import { setupServer } from "msw/node";
import { setupJestCanvasMock } from "jest-canvas-mock";
import App from "./App.svelte";

const date = new Date("2023-05-17T00:00:00");

const mockHiscoresByPlayers = [
  {
    hiscores: [
      {
        id: 1,
        new_exp: 2337,
        total_gained_exp: 1000,
        created_at: date,
        player_id: 1,
      },
      {
        id: 3,
        new_exp: 3337,
        total_gained_exp: 2000,
        created_at: new Date(date).setDate(date.getDate() + 1),
        player_id: 1,
      },
    ],
    player: {
      created_at: date,
      id: 1,
      name: "Elaine",
      original_exp: 1337,
    },
  },
  {
    hiscores: [
      {
        id: 2,
        new_exp: 350,
        total_gained_exp: 350,
        created_at: new Date(date).setDate(date.getDate() + 1),
        player_id: 2,
      },
    ],
    player: {
      created_at: date,
      id: 2,
      name: "Guybrush",
      original_exp: 0,
    },
  },
  {
    hiscores: [
      {
        id: 4,
        new_exp: 0,
        total_gained_exp: 0,
        created_at: new Date(date).setDate(date.getDate() + 1),
        player_id: 3,
      },
    ],
    player: {
      created_at: date,
      id: 3,
      name: "LeChuck",
      original_exp: 0,
    },
  },
  {
    hiscores: [],
    player: {
      created_at: new Date(date).setDate(date.getDate() + 1),
      id: 4,
      name: "Wally",
      original_exp: 0,
    },
  },
];

describe("App", () => {
  const server = setupServer(
    rest.get("/api/hiscores_by_players", (req, res, ctx) => {
      return res(ctx.status(200), ctx.json(mockHiscoresByPlayers));
    })
  );

  beforeAll(() => server.listen());
  beforeEach(() => {
    render(App);
    // jest.resetAllMocks();
    setupJestCanvasMock();
  });
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  it("should show page title", () => {
    const title = screen.getByText("OpenRSC overall experience tracker");
    expect(title).toBeInTheDocument();
  });

  it("should show loading text before mounting", () => {
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("should show cards with valid texts", async () => {
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).toBeNull();
      expect(screen.getByText("Elaine")).toBeInTheDocument();
      expect(
        screen.getByText("Gained exp since 5/17/2023: 2,000", { exact: false })
      ).toBeInTheDocument();
      expect(screen.getByText("Guybrush")).toBeInTheDocument();
      expect(
        screen.getByText("Gained exp since 5/18/2023: 350", { exact: false })
      ).toBeInTheDocument();
      expect(screen.getByText("LeChuck")).toBeInTheDocument();
      expect(
        screen.getByText("Gained exp since 5/18/2023: 0", { exact: false })
      ).toBeInTheDocument();
      expect(screen.getByText("Wally")).toBeInTheDocument();
      expect(screen.getByText("No data to show")).toBeInTheDocument();
    });
  });
});
