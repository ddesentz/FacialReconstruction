import { Instance, setLivelynessChecking, types } from "mobx-state-tree";

export const RootStore = types.model("RootStore", {
});

let rootStore: any;

export const defaultRootStore = (env?: any): IRootStore => {
  if (rootStore) {
    return rootStore;
  }

  rootStore = RootStore.create({}, env);
  if (
    (window.location && window.location.hostname === "localhost") ||
    window.location.hostname === "127.0.0.1"
  ) {
    setLivelynessChecking("error");
  }
  return rootStore;
};
export type IRootStore = Instance<typeof RootStore>;
