from client import TransformPipeline4x4
import math

def main():
    proj = TransformPipeline4x4.perspective(math.radians(60), 1.333, 0.1, 100.0)
    pt = [1.0, 1.0, -10.0]
    ndc = TransformPipeline4x4.project_point(proj, pt)
    print("4x4 Perspective Projection Verification:")
    print(f"World Point: {pt}")
    print(f"Projected NDC Point: {ndc}")

if __name__ == "__main__":
    main()
