# Collection of Nix Configurations

## Full System Config (NixOS)

In the current state, there exist 2 setup templates for NixOS.
In the current state, they are used as an input to a nixos-infect script updated for flake usage (https://https://github.com/AlexBarbatsalos/nixos-infect.git).

#### (1) ec2-small.nix
This is for AWS-ec2 instances. 

Current State:

The setup breaks with respect to nix handling AWS-instance support. ❌

```json

error: The option virtualisation.amazonGuest' does not exist. Definition values:
       - In /nix/store/jl66fjrrblsnkpca6ni8cm461vcb97g3-source/hosts/ec2-small.nix':
```

```json

error: path '/nix/store/kcmmd6alr3lx56vkf72503h3pxgf6iv4-source/nixos/modules/profiles/amazon-image.nix' does not exist
```


## Multishell

This directory includes several ephemeral shells for specific purposes.

They can be accessed from within the directory with ```nix develop .#<shell_name>```

| Shell_name | Description |
| --------   | -------     |
| default    | very basic packaging |
| networking | tools related to inspecting network traffic, firewalling, etc. |
| system_debug | tools for inspecting system behavior |
| full_debug | networking ++ system_debug |
| python_ds | several python libraries for Data Science and Machine Learning |
| haskell | very basic packages for executing haskell source code | 
| pentesting | networking ++ (several tools specific to pentesting) |

