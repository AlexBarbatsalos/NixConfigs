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

